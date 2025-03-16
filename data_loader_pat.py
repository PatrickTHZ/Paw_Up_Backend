import json
from dependencies import generate_embeddings, upsert_documents
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
def upload_from_json(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    prepared_data = []

    for company_id, company_data in data.items():
        company_name = company_data["Company"]
        insurance_policies = company_data["Insurance_Policies"]

        for policy_name, policy_details in insurance_policies.items():
            text = policy_details.get("general_info", "")
            chunks = text_splitter.split_text(text)

            for i, chunk in enumerate(chunks):

                metadata = {
                    "Company": company_name,
                    "Policy Name": policy_name,
                    "chunk_id": i,
                    "total_chunks": len(chunks),
                    "doc_id": f"{company_id}-{policy_name}"
                }

                prepared_data.append({
                    "id": f"{metadata['doc_id']}-{i}",
                    "values": generate_embeddings(chunk),
                    "metadata": metadata
                })

    upsert_documents(prepared_data)
    print(f"Uploaded {len(prepared_data)} chunks successfully!")

if __name__ == "__main__":
    upload_from_json("Data Source/updated_extracted_policies.json")
