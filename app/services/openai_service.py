from openai import AsyncOpenAI


def init_openAI():

    client = AsyncOpenAI()
    return client
