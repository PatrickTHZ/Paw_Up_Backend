import json
from dependencies import generate_embeddings, upsert_documents
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Initialize the text splitter for chunking text
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Size of each chunk
    chunk_overlap=50  # Overlap between chunks
)

def upload_from_json(json_file):
    # Open and load the JSON file
    with open(json_file, "r") as file:
        data = json.load(file)

    prepared_data = []  # List to store the prepared data to be uploaded

    # Loop through each article in the JSON (since it's a list of strings)
    for idx, article_content in enumerate(data):
        
        # Split the article into smaller chunks if it's too large
        chunks = text_splitter.split_text(article_content)

        # Loop through each chunk of text and prepare the metadata
        for i, chunk in enumerate(chunks):
            metadata = {
                "article_id": idx,  # Unique ID for each article
                "chunk_id": i,      # ID for each chunk
                "total_chunks": len(chunks),  # Total number of chunks for this article
                "doc_id": f"article-{idx}"  # Unique document ID for the article
            }

            # Prepare the data for upserting
            prepared_data.append({
                "id": f"{metadata['doc_id']}-{i}",  # Unique ID for each chunk
                "values": generate_embeddings(chunk),  # Embedding for the chunk
                "metadata": metadata  # Metadata about the chunk
            })

    # Upload the prepared data
    upsert_documents(prepared_data)
    print(f"Uploaded {len(prepared_data)} chunks successfully!")

if __name__ == "__main__":
    # Specify the path to your updated JSON file
    upload_from_json("Data Source/articles.json")
