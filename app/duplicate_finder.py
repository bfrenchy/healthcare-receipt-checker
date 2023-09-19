import os
import PyPDF2
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data/synthetic-receipts")
DEST_DIR = os.path.join(BASE_DIR, "../data")

df = pd.DataFrame(columns=['customer_name', 'address', 'city',
                           'state', 'zip_code', 'num_charges',
                           'num_duplicates', 'charges', 'duplicate_charges'])


def extract_text_from_pdf(pdf_path=DATA_DIR):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        if len(reader.pages) == 0:
            return ""
        page = reader.pages[0]
        return page.extract_text()


def find_duplicates(pdf_path=DATA_DIR):
    text = extract_text_from_pdf(pdf_path=pdf_path)
    charges = set()
    duplicates = set()
    lines = text.split('\n')

    customer_name = lines[lines.index('Customer Name:') + 1]
    address = lines[lines.index('Address:') + 1]
    city = lines[lines.index('City:') + 1]
    state = lines[lines.index('State:') + 1]
    zip_code = lines[lines.index('Zip:') + 1]

    for line in lines:
        if line.startswith('HC-'):
            charge = line.strip()  # Find the charge ID
            if charge in charges:
                duplicates.add(charge)
            else:
                charges.add(charge)
    charges_list = list(charges)
    duplicates_list = list(duplicates)

    df.loc[len(df)] = [customer_name, address, city, state, zip_code,
                       len(charges), len(duplicates),
                       charges_list, duplicates_list]


for filename in os.listdir(DATA_DIR):
    pdf_file_path = os.path.join(DATA_DIR, filename)
    find_duplicates(pdf_path=pdf_file_path)

df.to_csv(os.path.join(DEST_DIR, 'patient_data.csv'), index=False)
