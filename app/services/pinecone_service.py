import os
from pinecone import Pinecone, ServerlessSpec, PodSpec
import time

use_serverless = True

api_key = os.environ.get('PINECONE_API_KEY')
environment = os.environ.get('PINECONE_ENVIRONMENT') or 'us-west-2'


pinecone_index_name = os.environ.get("INDEX_NAME")


def connect_pinecone_init():
    pc = Pinecone(api_key=api_key)
    if use_serverless:
        spec = ServerlessSpec(cloud='aws', region='us-west-2')
    else:
        spec = PodSpec(environment=environment)

    existing_indexes = [
        index_info["name"] for index_info in pc.list_indexes()
    ]

    if pinecone_index_name not in existing_indexes:
        # if does not exist, create index
        pc.create_index(
            pinecone_index_name,
            dimension=1536,  # dimensionality of minilm
            metric="cosine",
            spec=spec
        )
        # wait for index to be initialized
        while not pc.describe_index(pinecone_index_name).status['ready']:
            time.sleep(1)
        print("Initialization Done")

    index = pc.Index(pinecone_index_name)
    time.sleep(1)
    return index
