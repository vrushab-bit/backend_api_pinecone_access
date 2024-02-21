from . import api
from app.services import index
from flask import jsonify, request


@api.route("/store", methods=["POST"])
def store():
    try:
        data = request.get_json()
        vectors = data.get("vectors", [])

        if not isinstance(vectors, list):
            return jsonify({"error": "Invalid data format: 'vectors' must be a list"}), 400

        res = index.upsert(
            vectors=vectors, namespace=data.get("namespace", "default"))
        return jsonify({"message": "Vectors stored successfully", "upserted_count": res["upserted_count"]}), 201
    except Exception as e:
        print(f"Error storing vectors: {e}")
        return jsonify({"error": "Internal server error"}), 500


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

        print(results)
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
