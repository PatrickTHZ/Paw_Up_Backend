import json
from dependencies import generate_embeddings, upsert_documents
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

def upload_reviews_from_json(json_file, company_name):
    with open(json_file, "r", encoding="utf-8") as file:
        reviews = json.load(file)

    prepared_data = []

    for i, review_obj in enumerate(reviews):
        review_text = review_obj["review"]
        label = review_obj["label"]
        score = review_obj["score"]

        chunks = text_splitter.split_text(review_text)

        for j, chunk in enumerate(chunks):
            metadata = {
                "Company": company_name,
                "chunk_id": j,
                "total_chunks": len(chunks),
                "doc_id": f"{company_name.lower()}-{i}",
                "label": label,
                "score": score
            }

            prepared_data.append({
                "id": f"{metadata['doc_id']}-{j}",
                "values": generate_embeddings(chunk),
                "metadata": metadata
            })

    upsert_documents(prepared_data)
    print(f"✅ Uploaded {len(prepared_data)} review chunks for {company_name}")

if __name__ == "__main__":
    upload_reviews_from_json("Data Source/medibank_reviews_sentiment.json", 'Medibank')
    upload_reviews_from_json("Data Source/rspca_reviews_sentiment.json", 'RSPCA')
