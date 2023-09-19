import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.platypus import Image, Table, TableStyle
import random

# Create the path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

template_path = os.path.join(BASE_DIR, "template.pdf")
logo_path = os.path.join(BASE_DIR, 'UCLA.png')


def create_synthetic_charges():
    num_charges = random.randint(3, 15)
    charges = [
        ['Charge ID',
         'Description',
         'Quantity',
         'Price',
         'Amount Billed']
    ]

    for _ in range(num_charges):
        charge_id = "HC-" + str(random.randint(2000, 10000))
        description = "Charge " + str(random.randint(1, 100))
        quantity = random.randint(1, 3)
        price = random.randint(50, 7500)
        total = quantity * price
        charges.append([charge_id,
                        description,
                        str(quantity),
                        "$" + str(price),
                        "$" + str(total)])

    if random.random() < 0.075:
        num_duplicates = random.randint(1, 3)
        for _ in range(num_duplicates):
            duplicate_charge = random.choice(charges[1:])
            charges.append(duplicate_charge)

    # Calculate total billed
    total_billed = sum(
        [int(charge[-1][1:].replace(",", "")) for charge in charges[1:]]
    )

    # Append the Total row
    charges.append(["", "", "", "Total:", f"${total_billed}"])
    return charges


def create_synthetic_patient():
    first_name = random.choice(["John", "Jane", "Michael", "Emily"])
    last_name = random.choice(["Doe", "Smith", "Johnson", "Brown"])
    address = (
        str(random.randint(1, 999)) +
        " " +
        random.choice(["Main", "Elm", "Oak"]) +
        " Street")
    city = random.choice(["New York", "Los Angeles", "Chicago", "Houston"])
    state = random.choice(["NY", "CA", "IL", "TX"])
    zip_code = random.choice(["10001", "90001", "60601", "77001"])

    customer_info = [
        ["Customer Name:", first_name + " " + last_name],
        ["Address:", address],
        ["City:", city],
        ["State:", state],
        ["Zip:", zip_code]
    ]

    return customer_info


def create_synthetic_receipt(pdf_path, logo_path=logo_path):
    charges = create_synthetic_charges()
    patient_info = create_synthetic_patient()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter
    )

    elements = []

    logo = Image(
        logo_path,
        width=80,
        height=40)
    elements.append(logo)
    elements.append(Spacer(1, 36))  # Add some space after the logo

    # Create a table for customer information
    patient_table = Table(patient_info)
    elements.append(patient_table)
    elements.append(Spacer(1, 12))  # Add some space after the table

    charges_table = Table(charges)
    charges_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'gray'),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), 'white'),
        ('TEXTCOLOR', (0, 1), (-1, -1), 'black'),
        ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('TOPPADDING', (0, -1), (-1, -1), 12),
    ]))
    elements.append(charges_table)

    doc.build(elements)


def create_pdfs(num_pdfs):
    i = 0
    while i < num_pdfs:
        pdf_path = os.path.join(
            BASE_DIR,
            f"../data/synthetic-receipts/PatientNo{i}.pdf")
        create_synthetic_receipt(pdf_path=pdf_path)
        i += 1


create_pdfs(num_pdfs=1500)
