from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.platypus import Image, Table, TableStyle

doc = SimpleDocTemplate("medical_bill.pdf", pagesize=letter)

elements = []

customer_info = [
    ["Customer Name:", "John Doe"],
    ["Address:", "123 Main Street"],
    ["City:", "New York"],
    ["State:", "NY"],
    ["Zip:", "10001"]
]

# Create a table for customer information
customer_table = Table(customer_info)
elements.append(customer_table)
elements.append(Spacer(1, 12))

logo = Image(
    "path",
    width=200,
    height=100)
elements.append(logo)
elements.append(Spacer(1, 36))
charges = [
    ["Description", "Quantity", "Price", "Total"],
    ["Consultation", "1", "$100", "$100"],
    ["Medication", "2", "$50", "$100"],
    ["Lab Test", "3", "$75", "$225"],
    ["Total", "", "", "$425"]
]

# Create a table for charges
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