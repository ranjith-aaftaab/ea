import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Email server configuration
SERVER = 'smtp.gmail.com'
PORT = 587
FROM_EMAIL = 'ranjithpython072@gmail.com'  # Replace with your email
PASSWORD = 'ptus saxt qigq edoe'       # Replace with your app-specific password

# Streamlit UI
st.title("Automated Email Invoice Tool")
st.write("Upload an Excel file with the required fields to send automated emails with invoices or reminders.")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas

def generate_proforma_invoice(data, pdf_path="proforma_invoice.pdf"):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Header Section - Logo and Company Info (Top Right)
    logo_path = "logo.png"  # Replace with your logo path
    c.drawImage(logo_path, width - 300, height - 100, width=300, height=120)
    
    
    #GST AND TITTLE
    c.drawCentredString(width / 2, height - 80, "PROFORMA INVOICE")
    c.drawRightString(width - 40, height - 100, "33ANPPP0425L2ZS")
    c.setFont("Helvetica-Bold", 20)
    
    
    # Date at right
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 40, height - 130, f" Date: {data['Proforma Date']}")

    # "To" Section (Recipient Details)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, height - 115, "TO:")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 130, f"{data['Company Name']}")
    c.drawString(40, height - 145, f"{data['Address City/District']}, {data['State']}, {data['Pincode']}")

    #PEROFRMA SUB
    c.setFont('Helvetica',12)
    c.drawString(60,height - 230,f"SUB: PROFORMA INVOICE TOWARDS RENEWAL {data['Website url']}")

    
    # Product Data with Example
    product_data = [
        ["SL No.", "Description", "Amount"],
        ["01", data['Item Description'], f"Rs. {data['Net Amount']}"]
    ]
    product_table = Table(product_data, colWidths=[40, 360, 100])
    product_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
    ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Center-align "SL No." column
    ('ALIGN', (2, 1), (2, -1), 'RIGHT'),  # Right-align "Amount" column
    ('VALIGN', (1, 1), (1, -1), 'TOP'),  # Align "Description" column text to the top
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('TOPPADDING', (0, 1), (-1, 1), 40),  # Increase top padding only for the second row
    ('BOTTOMPADDING', (0, 1), (-1, 1), 40),  # Increase bottom padding only for the second row
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Background for all rows except the header
    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid for the entire table
    ]   ))

    product_table.wrapOn(c, 40, height - 350)
    product_table.drawOn(c, 40, height - 400)


    # Financial Summary (Right-Aligned)
    c.setFont("Helvetica", 14)
    c.drawRightString(width - 70, height - 500, f"Net Amount: Rs. {data['Net Amount']}")
    c.drawRightString(width - 70, height - 515, f"CGST ({data['CGST Percent']}%): Rs. {data['CGST Amount']}")
    c.drawRightString(width - 70, height - 530, f"SGST ({data['SGST Percent']}%): Rs. {data['SGST Amount']}")
    c.drawRightString(width - 70, height - 545, f"Gross Total: Rs. {data['Gross Amount']}")


  


    # Footer Message (Bold, Centered)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, 150, "Awaiting your payment at the earliest.")
    c.drawCentredString(width / 2, 125, "Please renew promptly to avoid service interruption.")
    c.drawCentredString(width /2, 85, "Archer Websol,Door No: 8/19, Annal Gandhi Cross Street,Vetrinagar, Perambur, Chennai-600082 ,\nEmail: archerwebsol2024@gmail.com,Phone: +91-44-48588105, +91-8056109699, +91-9790740735")

    # Save the PDF
    c.save()

    return pdf_path


if uploaded_file:
    email_data = pd.read_excel(uploaded_file)
    
    # Convert date columns to datetime format
    email_data['Bill Date'] = pd.to_datetime(email_data['Bill Date'], errors='coerce')
    email_data['Invoice Date'] = pd.to_datetime(email_data['Invoice Date'], errors='coerce')
    email_data['Date Order'] = pd.to_datetime(email_data['Date Order'], errors='coerce')
    email_data['Date Registration'] = pd.to_datetime(email_data['Date Registration'], errors='coerce')
    email_data['Proforma Date'] = pd.to_datetime(email_data['Proforma Date'], errors='coerce')
    # Add more date columns as needed

    st.write("Data Preview:")
    st.dataframe(email_data)

    required_columns = {'Company Name', 'GST Number', 'Address City/District', 'Pincode', 'State',
                        'Contact Person', 'Contact Number', 'Contact Email', 'Item Description', 'Bill Number',
                        'Bill Date', 'Date Order', 'Date Registration', 'Place Client', 'Website url', 'Net Amount',
                        'IGST percent', 'IGST Amount', 'CGST Percent', 'CGST Amount', 'SGST Percent', 'SGST Amount',
                        'Gross Amount', 'Payment Method', 'Payment Detail', 'Payment Status', 'Proforma Date',
                        'Proforma For', 'Period', 'Invoice Number', 'Invoice Date', 'Admin Remarks', 'has_paid'}
    
    if not required_columns.issubset(email_data.columns):
        st.error("The uploaded file must contain the specified columns.")
    else:
        if st.button("Send Emails"):
            try:
                server = smtplib.SMTP(SERVER, PORT)
                server.starttls()
                server.login(FROM_EMAIL, PASSWORD)
                today = datetime.now().date()

                for i, row in email_data.iterrows():
                    data = row.to_dict()  # Convert row data to dictionary for easy access
                    email = data['Contact Email']
                    invoice_number = data['Invoice Number']

                    if data['has_paid'].strip().lower() == 'no':
                        # Generate reminder email content
                        message_body = f"""
                        Dear {data['Contact Person']},

                        Greetings from Archer Websol...

                        Please find the attached proforma invoice for the renewal of your website for the period {data['Period']}.

                        Kindly renew in time to avoid expiry and release payment ASAP.

                        Regards,
                        SUPPORT TEAM
                        """

                        msg = MIMEMultipart()
                        msg['From'] = FROM_EMAIL
                        msg['To'] = email
                        msg['Subject'] = 'Payment Reminder'
                        msg.attach(MIMEText(message_body, 'plain'))

                        # Generate PDF invoice
                        pdf_path = generate_proforma_invoice(data, invoice_number)
                        with open(pdf_path, 'rb') as pdf_file:
                            pdf = MIMEApplication(pdf_file.read(), _subtype="pdf")
                            pdf.add_header('Content-Disposition', 'attachment', filename=f'Invoice_{invoice_number}.pdf')
                            msg.attach(pdf)

                        # Send email
                        server.sendmail(FROM_EMAIL, email, msg.as_string())
                        st.success(f'Reminder email sent to {data["Contact Person"]} ({email}) with dynamic invoice.')

                        # Clean up generated PDF
                        os.remove(pdf_path)

                    elif data['has_paid'].strip().lower() == 'yes':
                        # Generate invoice email content
                        invoice_message = f"""
                        Hi {data['Contact Person']},
                        
                        Thank you for your payment. Please find attached the invoice for your records.
                        
                        Regards,
                        SUPPORT TEAM
                        """

                        msg = MIMEMultipart()
                        msg['From'] = FROM_EMAIL
                        msg['To'] = email
                        msg['Subject'] = 'Payment Invoice'
                        msg.attach(MIMEText(invoice_message, 'plain'))


                server.quit()
                st.success("All applicable emails sent successfully.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
