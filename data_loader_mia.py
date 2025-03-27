import json
from dependencies import generate_embeddings, upsert_documents


def upload_from_json(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    prepared_data = []

    for idx, inData in enumerate(data):
        plan_Details = (
            f"Company ID: {inData['Company_ID']}\n"
            f"Company Name: {inData['Company Name']}\n"
            f"Plan Name: {inData['Plan Name']}\n"
            f"Furry friend: {inData['Furry Friend']}\n"
            f"Annual limit: {inData['Annual limit']}\n"
            f"Eligible vet bill reimbursement: {inData['Eligible vet bill reimbursement']}\n"
            f"Age eligibility: {inData['Age eligibility']}\n"
            f"Annual condition limit: {inData['Annual condition limit']}\n"
            f"Specified accidental injuries and illnesses: {inData['Specified accidental injuries and illnesses']}\n"
            f"Multi-pet discount: {inData['Multi-pet discount']}\n"
            f"Tick paralysis: {inData['Tick paralysis']}\n"
            f"Emergency boarding fees: {inData['Emergency boarding fees']}\n"
            f"Consultations and vet visits benefits: {inData['Consultations and vet visits benefits']}\n"
            f"Cruciate ligament conditions benefits: {inData['Cruciate ligament conditions benefits']}\n"
            f"Waiting periods: {inData['Waiting periods']}\n"
            f"Cancer treatment: {inData['Cancer treatment']}\n"
            f"Skin conditions: {inData['Skin conditions']}\n"
            f"Hereditary and congenital conditions: {inData['Hereditary and congenital conditions']}\n"
            f"Eye and ear conditions: {inData['Eye and ear conditions']}\n"
            f"Essential euthanasia: {inData['Essential euthanasia']}\n"
            f"Pet overseas travel insurance (New Zealand and the Norfolk Islands only): {inData['Pet overseas travel insurance (New Zealand and the Norfolk Islands only)']}\n"
            f"Certain pre-existing conditions: {inData['Certain pre-existing conditions']}\n"
            f"Dental procedures: {inData['Dental procedures']}\n"
            f"Behavioural problems: {inData['Behavioural problems']}\n"
            f"Elective treatments and procedures: {inData['Elective treatments and procedures']}\n"
            f"Food and diets: {inData['Food and diets']}\n"
            f"Grooming: {inData['Grooming']}\n"
            f"Pregnancy: {inData['Pregnancy']}\n"
            f"Pet accessories: {inData['Pet accessories']}\n"
            f"Heartworm test or blood screen: {inData['Heartworm test or blood screen']}\n"
            f"FeLV/FIV test or urinalysis: {inData['FeLV/FIV test or urinalysis']}\n"
            f"De-sexing and Micro-chipping: {inData['De-sexing and Micro-chipping']}\n"
            f"Vaccinations: {inData['Vaccinations']}\n"
            f"Alternative therapies: {inData['Alternative therapies']}\n"
            f"Heartworm preventative medication: {inData['Heartworm preventative medication']}\n"
            f"Council registration fees: {inData['Council registration fees']}\n"
            f"Teeth cleaning: {inData['Teeth cleaning']}\n"
            f"Prescription diets: {inData['Prescription diets']}\n"
            f"Excess: {inData['Excess']}\n"
            f"Hip joint surgery: {inData['Hip joint surgery']}\n"
            f"Cremation or burial: {inData['Cremation or burial']}\n"
            f"Flea/tick/worm control: {inData['Flea/tick/worm control']}\n"
        )


        prepared_data.append({"values": generate_embeddings(plan_Details)})

    upsert_documents(prepared_data)
    print(f"Uploaded {len(prepared_data)} chunks successfully!")

if __name__ == "__main__":
    upload_from_json("Data Source/insurance_data.json")
