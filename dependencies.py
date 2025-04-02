import logging
import openai
import os
from pinecone import Pinecone
from config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    OPENAI_API_KEY
)

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Pinecone v4
pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index(PINECONE_INDEX_NAME)

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

def generate_embeddings(text: str):
    try:
        logging.info(f"Generating embedding for: {text[:50]}...")
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        logging.info("Embedding successful.")
        return response["data"][0]["embedding"]
    except openai.error.OpenAIError as e:
        logging.error(f"Embedding API Error: {e}")
        return None

def upsert_documents(documents: list, batch_size=50):
    try:
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            pinecone_index.upsert(vectors=batch)
            logging.info(f"Uploaded batch {i // batch_size + 1} of {(len(documents) - 1) // batch_size + 1}")
    except Exception as e:
        logging.error(f"Error during upsert: {e}")
