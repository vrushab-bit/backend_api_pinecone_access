from langchain.text_splitter import NLTKTextSplitter
from . import api
from flask import jsonify, request
import json
import uuid
from app.services import index, client, s3


# load_dotenv()
BUCKET_NAME = "transcribe-bucket-1339"


async def create_embeddings(sentences):
    for sentence in sentences:
        response = await client.embeddings.create(
            input=sentence,
            model="text-embedding-3-small",
            dimensions=1536
        )
        embedding = response.data[0].embedding
        upsert_pine(embedding, sentence=sentence)
    return


def upsert_pine(vector, sentence):
    upsert_response = index.upsert(
        vectors=[
            {
                'id': str(uuid.uuid4()),
                'values': vector,
                'metadata': {'sentence': sentence},
            },
        ],
        namespace='motion'
    )
    print("Inserted")
    return upsert_response


@api.route("/store", methods=["POST"])
async def store():
    data = request.get_json()

    if data["uid"].split(".")[1] != "txt":
        # print("in first try")
        return jsonify({"error": "Invalid data format: Data Format Invalid"})

    obj = s3.Object(BUCKET_NAME, data["uid"])
    file_content = obj.get()['Body'].read().decode('utf-8')

    data = json.loads(file_content)

    transcript = data["results"]["transcripts"][0]["transcript"]
    text_splitter = NLTKTextSplitter()
    docs = text_splitter.split_text(transcript)
    docs = docs[0].split("\n\n")

    await create_embeddings(docs)
    return jsonify({"message": docs}), 201


@api.route("/query", methods=["POST"])
def query():
    try:
        data = request.get_json()
        vectors = data.get("vectors", [])
        if not isinstance(vectors, list):
            return jsonify({"error": "Invalid data format: 'vectors' must be a list"}), 400

        namespace = data.get("namespace", "default")

        results = index.query(
            vector=vectors, top_k=3, namespace=namespace, include_metadata=True, include_values=True
        )

        # print(results)
        processed_results = [
            {
                "id": result["id"],
                "values": result["values"],
                "metadata": result["metadata"],
                "score": result["score"]
            }
            for result in results.matches
        ]
        return jsonify({"results": processed_results})
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return jsonify({"error": "Internal server error"}), 500
