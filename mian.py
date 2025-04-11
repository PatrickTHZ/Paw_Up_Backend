import random
import json
import logging
import openai
import requests
from dependencies import generate_embeddings, pinecone_index
from langchain_community.chat_message_histories import ChatMessageHistory
logging.basicConfig(level=logging.INFO)

SESSION_ID = "default-session"

def build_reference_context(metadata: dict) -> str:
    if "text" in metadata and metadata["text"]:
        return metadata["text"]

    keys = ["Company", "Company Name", "Policy Name", "Plan Name", "Furry Friend", "doc_id"]
    parts = [f"{key}: {metadata[key]}" for key in keys if key in metadata and metadata[key]]
    return "; ".join(parts)

def query_pinecone(vector, top_k=3):
    try:
        results = pinecone_index.query(vector=vector, top_k=top_k, include_metadata=True)
        return results.get("matches", [])
    except Exception as e:
        logging.error(f"Error querying Pinecone: {e}")
        return []

def generate_response(query: str):
    try:
        history = ChatMessageHistory()
        chat_history = history.messages

        query_vector = generate_embeddings(query)
        pinecone_result = query_pinecone(query_vector, top_k=3) if query_vector else []
        logging.info(f"Pinecone retrieval result: {pinecone_result}")

        reference_context = build_reference_context(pinecone_result[0].get("metadata", {})) if pinecone_result else ""
        logging.info(f"Reference context: {reference_context}")

        if reference_context:
            system_message = f"""
You are Paw-up, a fun and friendly chatbot for Paw-up! Your job is to help users understand what pet insurance is by looking at the context from Pinecone-retrieved data, answer customer inquiries, and handle errors in a friendly and engaging way.
When answering the following question, please use ONLY the provided context if it is relevant.
Context: {reference_context}
If the context is not relevant, then answer in your usual style.
"""
        else:
            system_message = """
You are Paw-up, a fun and friendly chatbot for Paw-up! Your job is to help users understand what pet insurance is, answer customer inquiries, and handle errors in a friendly and engaging way.
"""

        messages = [{"role": "system", "content": system_message}]
        messages.extend([m.dict() for m in chat_history])
        messages.append({"role": "user", "content": query})

        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        openai_reply = openai_response["choices"][0]["message"]["content"]
        logging.info(f"OpenAI reply: {openai_reply}")

        # Save new messages to memory
        history.add_user_message(query)
        history.add_ai_message(openai_reply)

        return {
            "pinecone_result": pinecone_result,
            "reference_context": reference_context,
            "openai_response": openai_reply
        }

    except Exception as e:
        logging.error(f"Error in generate_response: {e}")
        return {"response": "An error occurred while processing your request."}

if __name__ == "__main__":
    user_query = input("Enter your question: ")
    result = generate_response(user_query)

    if "pinecone_result" in result:
        print("Pinecone Retrieval Result:")
        print(result["pinecone_result"])
    if "reference_context" in result:
        print("\nReference Context:")
        print(result["reference_context"])
    if "openai_response" in result:
        print("\nResponse from OpenAI model:")
        print(result["openai_response"])
    elif "response" in result:
        print("Response:", result.get("response", "No response available."))
