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

    for idx, policy in enumerate(data):
        policy_name = policy["Insurance Cover"].replace("PROMOTED\n", "").replace("Finder Award", "").replace("Exclusive", "").replace("Highly Commended", "").replace("Best Rated Brand", "").strip()

        max_yearly_benefit = policy["Maximum Yearly Benefit"]
        if not max_yearly_benefit or str(max_yearly_benefit).lower() in ['no', 'null']:
            max_yearly_benefit = "Not Specified"

        reimbursement_rate = policy["Reimbursement Rate %"]
        if not reimbursement_rate:
            reimbursement_rate = "Not Specified"

        policy_text = (
            f"Accidental Injury Cover: {'Yes' if policy['Accidental Injury Cover'] else 'No'}\n"
            f"Illness Cover: {'Yes' if policy['Illness Cover'] else 'No'}\n"
            f"Paralysis Tick yearly sub-limit: {policy['Paralysis Tick yearly sub-limit']}\n"
            f"Maximum Yearly Benefit: {max_yearly_benefit}\n"
            f"Reimbursement Rate: {reimbursement_rate}\n"
            f"Bonus: {policy['Bonus']}"
        )

        chunks = text_splitter.split_text(policy_text)

        for i, chunk in enumerate(chunks):
            metadata = {
                "Policy Name": policy_name,
                "chunk_id": i,
                "total_chunks": len(chunks),
                "doc_id": f"policy-{idx}"
            }

            prepared_data.append({
                "id": f"{metadata['doc_id']}-{i}",
                "values": generate_embeddings(chunk),
                "metadata": metadata
            })

    upsert_documents(prepared_data)
    print(f"Uploaded {len(prepared_data)} chunks successfully!")

if __name__ == "__main__":
    upload_from_json("Data Source/finder_data.json")
