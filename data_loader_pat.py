import json
import logging
from dependencies import generate_embeddings, upsert_documents, test_pinecone_connection

def upload_from_json(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    prepared_data = []

    for i, entry in enumerate(data):

        doc_id = f"{entry.get('company_id', 'unknown')}-{entry.get('plan_name', 'unknown').replace(' ', '_')}-{i}"

        text = f"""
        Plan: {entry.get('plan_name')}
        Company: {entry.get('company_name')}
        Annual Limit: {entry.get('annual_limit')}
        Vet Bill Reimbursement: {entry.get('eligible_vet_bill_reimbursement')}
        Age Eligibility: {entry.get('age_eligibility')}
        Monthly: {entry.get('plan_monthly')}
        Yearly: {entry.get('plan_yearly')}
        Cancer Treatment: {entry.get('cancer_treatment')}
        Conditions: {entry.get('specified_accidental_injuries_and_illnesses')}
        """

        # Generate embedding
        embedding = generate_embeddings(text)
        if embedding:
            cleaned_metadata = {k: v for k, v in entry.items() if v is not None}
            prepared_data.append({
                "id": doc_id,
                "values": embedding,
                "metadata": cleaned_metadata
            })

    upsert_documents(prepared_data)
    logging.info(f"Uploaded {len(prepared_data)} documents to Pinecone.")

if __name__ == "__main__":
    test_pinecone_connection()
    upload_from_json("centralised_cleaned_data 1.json")
