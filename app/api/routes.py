from . import api
from app.services import index
from flask import jsonify, request


@api.route("/store", methods=["POST"])
def store():

    upsert_response = index.upsert(
        vectors=[
            {'id': 'vec1',
             'values': [0.1, 0.2, 0.3],
             'metadata': {'genre': 'drama'},
             'sparse_values': {
                 'indices': [10, 45, 16],
                 'values': [0.5, 0.5, 0.2]
             }},
            {'id': 'vec2',
             'values': [0.2, 0.3, 0.4],
             'metadata': {'genre': 'action'},
             'sparse_values': {
                 'indices': [15, 40, 11],
                 'values': [0.4, 0.5, 0.2]
             }}
        ],
        namespace='example-namespace'
    )

    return jsonify({"message": "Success"})


@api.route("/query", methods=["POST"])
def query():
    embeddings = request.json["query-embeddings"]

    res = index.query(vector=embeddings, top_k=3,
                      include_values=True, include_metadata=True)

    print(res.matches)
    return jsonify({"messgage": "retrieved"})
