from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_proforma_invoice(data, pdf_path="proforma_invoice.pdf"):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Title Section - Proforma Invoice Title and Date
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 80, "PROFORMA INVOICE")
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 40, height - 100, f"DATE: {data['Invoice Date']}")

    # Recipient Information (TO Section)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, height - 140, "TO:")
    c.setFont("Helvetica", 10)
    c.drawString(80, height - 140, data['Company Name'])
    c.drawString(80, height - 155, data['Company Address'])
    c.drawString(80, height - 170, data['City and State'])

    # Client GST Number
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, height - 200, "CLIENT GST NUMBER:")
    c.setFont("Helvetica", 10)
    c.drawString(180, height - 200, data['Client GST Number'])

    # Subject Line
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 230, f"SUB: PROFORMA INVOICE FOR RENEWAL - {data['Invoice Year']}")

    # Website Renewal Details Information
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 250, "PLEASE FIND BELOW THE DETAILS FOR TOWARDS RENEWAL OF WEBSITE")

    # Table for Service Details
    service_data = [
        ["SL NO.", "DESCRIPTION", "AMOUNT"],
        ["01", f"Domain and Hosting renewal for the website\nfor the period of Oct 2024 to Sep 2025\n{data['Website URL']}", f"Rs. {data['Amount']}"]
    ]
    table = Table(service_data, colWidths=[40, 360, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (2, 1), (2, 1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (1, 1), (1, 1), 'TOP'),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Positioning and Drawing the Table
    table_y_position = height - 330
    table.wrapOn(c, 40, table_y_position)
    table.drawOn(c, 40, table_y_position)

    # Financial Summary
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - 40, height - 450, f"Net Amount: Rs. {data['Amount']}")
    c.drawRightString(width - 40, height - 465, f"GST ({data['GST Percent']}%): Rs. {data['GST Amount']}")
    c.drawRightString(width - 40, height - 480, f"Gross Total: Rs. {data['Gross Amount']}")
    c.drawRightString(width - 40, height - 495, f"ROUND OFF: RS. {data['Rounded Amount']}")

    # Footer Company Details
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, 100, "Archer Websol")
    c.drawCentredString(width / 2, 85, "Door No: 8/19, Annal Gandhi Cross Street, Vetrinagar, Perambur, Chennai-600082")
    c.drawCentredString(width / 2, 70, "Phone: +91-44-48588105, +91-8056109699, +91-9790740735")
    c.drawCentredString(width / 2, 55, "Email: contact@archerwebsol.com, GST NO.: 33ANPPP0425L2ZS")

    # Additional Footer Notes
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, 35, "Awaiting your payment at the earliest.")
    c.drawCentredString(width / 2, 20, "Please renew promptly to avoid service interruption.")

    # Save the PDF
    c.save()
    return pdf_path
