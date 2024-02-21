from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()
# print(os.environ['PINECONE_API_KEY'])

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
