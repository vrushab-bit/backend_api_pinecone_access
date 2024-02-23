from .pinecone_service import connect_pinecone_init
from .openai_service import init_openAI
from .s3 import initialze_s3

index = connect_pinecone_init()
client = init_openAI()
s3 = initialze_s3()
