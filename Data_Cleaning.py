from pinecone import Pinecone

api_key = "c29316cb-d757-4add-a5ea-6d6ed9a44397"
index_name = "pawup"

pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

# Delete all vectors in the index
index.delete(delete_all=True)
print(f"All vectors deleted from '{index_name}'.")
