import json
from dependencies import generate_embeddings, upsert_documents
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def upload_plan_details(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    prepared_data = []

    for i, entry in enumerate(data):
        text = "\n".join([f"{k}: {v}" for k, v in entry.items()])
        chunks = text_splitter.split_text(text)

        for j, chunk in enumerate(chunks):
            metadata = {
                "Company_ID": entry.get("Company_ID"),
                "Company Name": entry.get("Company Name"),
                "Plan Name": entry.get("Plan Name"),
                "Furry Friend": entry.get("Furry Friend"),
                "chunk_id": j,
                "total_chunks": len(chunks)
            }

            prepared_data.append({
                "id": f"{entry.get('Company_ID')}-{entry.get('Plan Name').replace(' ', '_')}-{j}",
                "values": generate_embeddings(chunk),
                "metadata": metadata
            })

    upsert_documents(prepared_data)
    print(f"Uploaded {len(prepared_data)} chunks from plan details.")

def load_optional_extras(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    optional_lookup = {}
    for item in data:
        key = (
            item["Company_ID"],
            item["Company Name"],
            item["Furry Friend"],
            item["Optional Extra Name"]
        )
        optional_lookup[key] = {
            "Fortnightly": item["Fortnightly"],
            "Monthly": item["Monthly"],
            "Yearly": item["Yearly"]
        }

    print(f"Loaded {len(optional_lookup)} optional extras.")
    return optional_lookup

def load_payment_data(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    payments = {}
    for item in data:
        key = (
            item["Company_ID"],
            item["Company Name"],
            item["Furry Friend"],
            item["Plan Name"],
            item["Age"],
            item.get("Gender"),
            item.get("De-sexed")
        )
        payments[key] = {
            "Fortnightly": item["Fortnightly"],
            "Monthly": item["Monthly"],
            "Yearly": item["Yearly"]
        }

    print(f"Loaded {len(payments)} payment entries.")
    return payments

if __name__ == "__main__":
    upload_plan_details("Data Source/insurance_data.json")
    optional_extras = load_optional_extras("Data Source/insurance_data_optional.json")
    payment_data = load_payment_data("Data Source/insurance_data_payment.json")