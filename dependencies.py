import smtplib
import random
import openai
import json
import logging
from pinecone import Pinecone
from config import (PINECONE_API_KEY, PINECONE_INDEX_NAME, OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
openai.api_key = OPENAI_API_KEY
pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index(PINECONE_INDEX_NAME)

def generate_embeddings(text: str):
    try:
        logging.info(f"Generating: {text[:50]}...")
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        logging.info("Embedding successful.")
        return response["data"][0]["embedding"]
    except Exception as e:
        logging.error(f"Embedding API Error: {e}")
        return None

def upsert_documents(documents: list, batch_size=50):
    try:
        valid_docs = [doc for doc in documents if doc.get("values") and isinstance(doc["values"], list)]

        if not valid_docs:
            logging.warning("No valid documents to upsert.")
            return

        for i in range(0, len(valid_docs), batch_size):
            batch = valid_docs[i: i + batch_size]
            # Optional: log first vector of the batch
            logging.info(f"Upserting batch {i // batch_size + 1} with {len(batch)} vectors")
            logging.debug(json.dumps(batch[0], indent=2))  # Comment this if it's too big

            pinecone_index.upsert(vectors=batch)

        logging.info(f"Successfully uploaded {len(valid_docs)} documents to Pinecone.")
    except Exception as e:
        logging.error(f"Pinecone Upsert Error: {e}")

def test_pinecone_connection():
    try:
        result = pinecone_index.describe_index_stats()
        logging.info("Pinecone index connection successful.")
        logging.info(f"Index stats: {result}")
    except Exception as e:
        logging.error(f"Failed to connect to Pinecone: {e}")

