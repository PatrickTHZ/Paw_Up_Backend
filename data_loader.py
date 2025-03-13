import json
from dependencies import generate_embeddings, upsert_documents

def upload_from_json(json_file):

    with open(json_file, "r") as file:
        data = json.load(file)

    prepared_data = []

    for company_id, company_data in data.items():
        company_name = company_data["Company"]
        insurance_policies = company_data["Insurance_Policies"]

        for policy_name, policy_details in insurance_policies.items():
            prepared_data.append({
                "id": f"{company_id}-{policy_name}",
                "values": generate_embeddings(policy_details["general_info"]),
                "metadata": {
                    "Company": company_name,
                    "Policy Name": policy_name,
                    **policy_details  \
                }
            })

    upsert_documents(prepared_data)
    print(f"Uploaded {len(prepared_data)} \ successful!")


if __name__ == "__main__":
    upload_from_json("updated_extracted_policies.json")