import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import os

# Email server configuration
SERVER = 'smtp.gmail.com'
PORT = 587
FROM_EMAIL = os.environ.get('FROM_EMAIL')  # Fetches the FROM_EMAIL value
PASSWORD = os.environ.get('PASSWORD')      # Fetches the PASSWORD value
# Replace with your app-specific password

# Streamlit UI
st.title("Automated Email Invoice Tool")
st.write("Upload an Excel file with the required fields to send automated emails with invoices or reminders.")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

# Function to generate the PDF invoice with a static table height and word wrapping
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_proforma_invoice(data, pdf_path="proforma_invoice.pdf"):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    #bOTTOM

    
    #IMAGE LOGO
    logo_path = "logo6.png"  # Replace with your logo path
    c.drawImage(logo_path, width - 170, height -80, width=150, height=60)

    # Title Section - Proforma Invoice Title and Date
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(width / 2, height - 80, "PROFORMA INVOICE")
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 30, height - 130, f"DATE: {data['Proforma Date']}")

    # Recipient Information (TO Section)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, height - 130, "TO")
    c.setFont("Helvetica", 10)
    c.drawString(40,height - 145,data['Company Name'])
    c.drawString(40, height - 160,data['Address'])
    c.drawString(40, height - 175,data['Pincode'])
    # Client GST Number

    # Subject Line
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 220, f"SUB: PROFORMA INVOICE FOR RENEWAL - {data['Period']}")
    c.drawCentredString(width / 2, height - 235,data['Website url'])

    # Website Renewal Details Information
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 280, "PLEASE FIND BELOW DETAILS TOWARDS RENEWAL OF WEBSITE")

    # Table for Service Details
    service_data = [
        ["SL NO.", "DESCRIPTION", "AMOUNT"],
        [
            "01",
            f"{data['Item Description']}\n",f"Rs. {data['Net Amount']}"            
            ""
        ],
        [
            "", 
            "Net Amount:\nGST:\nGross Amount:", 
            f"Rs. {data['Net Amount']}\nRs. {data['GST Amount']}\nRs. {data['Gross Amount']}"
        ]
    ]
    
    table = Table(service_data, colWidths=[40, 400, 80])

# Apply styles with specific alignments for different cells
    table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    
    # Center-align the first row for headers
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    
    # Center-align all cells by default
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),

    # Specific alignment for "DESCRIPTION" column rows
    ('ALIGN', (1, 1), (1, 1), 'LEFT'),   # Left-align the first data row in "DESCRIPTION"
    ('ALIGN', (1, 2), (1, 2), 'RIGHT'),  # Right-align the second data row in "DESCRIPTION"
    
    # Set font and size
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    
    # Vertically align all cells to the middle
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

    # Add padding for readability
    ('TOPPADDING', (0, 1), (-1, -1), 10),
    
    # Add grid to all cells
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))


    # Positioning and Drawing the Table
    table_y_position = height - 450
    table.wrapOn(c, 40, table_y_position)
    table.drawOn(c, 40, table_y_position)


    #RUPEES IN WORDS
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 465, f"({data['Rupees']})")

    #GREETING BEXT
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2,285 , "Awaiting your payment at the earliest.")
    c.drawCentredString(width / 2,270 , "Please You are requested to renew the wbsite in time to avoid EXPIRY")



    bottom_path = "bottom2.png"  # Replace with your logo path
    c.drawImage(bottom_path, width - 590, height - 790, width=585, height=250)


    c.drawCentredString(width /2, 30, "Archer Websol,Door No: 8/19, Annal Gandhi Cross Street,Vetrinagar, Perambur, Chennai-600082 ,")
    c.drawCentredString(width /2,15 ,"Email: archerwebsol2024@gmail.com,Phone: +91-44-48588105, +91-8056109699, +91-9790740735")
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 27, height - 790,"** This is online auto generated proforma invoice **")
    # Save the PDF
    c.save()
    return pdf_path

    
if uploaded_file:
    email_data = pd.read_excel(uploaded_file)
    
    # Convert date columns to datetime format

    email_data['Proforma Date'] = pd.to_datetime(email_data['Proforma Date'], errors='coerce').dt.strftime('%d-%m-%Y')

    # Add more date columns as needed

    st.write("Data Preview:")
    st.dataframe(email_data)

    required_columns = {'Company Name', 'GST Number', 'Address', 'Pincode', 'State',
                        'Contact Email', 'Item Description','Proforma Date','Website url', 'Net Amount',
                        'GST Amount','Gross Amount','Period','has_paid','Rupees'}

    
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

                    if data['has_paid'].strip().lower() == 'no':
                        # Generate reminder email content
                        message_body = f"""
                        Dear Sir/Madam,

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
                        name = data['Company Name']
                        pdf_path = generate_proforma_invoice(data, name)
                        with open(pdf_path, 'rb') as pdf_file:
                            pdf = MIMEApplication(pdf_file.read(), _subtype="pdf")
                            pdf.add_header('Content-Disposition', 'attachment', filename=f'Proforma Invoice_{name}.pdf')
                            msg.attach(pdf)

                        # Send email
                        server.sendmail(FROM_EMAIL, email, msg.as_string())
                        st.success(f'Reminder email sent to {data["Company Name"]} ({email}) with dynamic invoice.')

                        # Clean up generated PDF
                        os.remove(pdf_path)

                    elif data['has_paid'].strip().lower() == 'yes':
                        # Generate invoice email content
                        invoice_message = f"""
                        Hi {data['Company Name']},
                        
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
