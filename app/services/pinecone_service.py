import os
from pinecone import Pinecone, ServerlessSpec, PodSpec
import time

# use_serverless = os.environ.get("USE_SERVERLESS", "False").lower() == "true"
use_serverless = True
# api_key = os.environ['PINECONE_API_KEY'] or 'PINECONE_API_KEY'
api_key = "2420befc-9b06-4c28-870d-942519746ce8"
environment = os.environ.get('PINECONE_ENVIRONMENT') or 'PINECONE_ENVIRONMENT'
# print(api_key)


pinecone_index_name = "motion-ask"


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
            dimension=3,  # dimensionality of minilm
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
