import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Email server configuration
SERVER = 'smtp.gmail.com'
PORT = 587
FROM_EMAIL = 'ranjithpython072@gmail.com'  # Replace with your email
PASSWORD = 'ptus saxt qigq edoe'       # Replace with your app-specific password

# Streamlit UI
st.title("Email Automation Tool")
st.write("Upload an Excel file with fields such as Full Name, Email Address, Remainder Date, Due Date, Amount, and Has (Has_Paid)")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    # Load and preview the data
    email_data = pd.read_excel(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(email_data)

    # Check if essential columns are present
    required_columns = {'Full name', 'Email Address', 'Remainder Date', 'Due Date', 'Amount', 'Has'}
    if not required_columns.issubset(email_data.columns):
        st.error("The uploaded file must contain the following columns: Full name, Email Address, Remainder Date, Due Date, Amount, Has")
    else:
        # Compose and send emails
        if st.button("Send Emails"):
            try:
                # Set up SMTP server
                server = smtplib.SMTP(SERVER, PORT)
                server.starttls()
                server.login(FROM_EMAIL, PASSWORD)

                # Current date for comparison
                today = datetime.now().date()

                # Iterate over the rows and send emails
                for i, row in email_data.iterrows():
                    # Skip if Has (Has_Paid) is No
                    if row['Has'].strip().lower() == 'no':
                        # Retrieve details for reminder email
                        name = row['Full name']
                        email = row['Email Address']
                        remainder_date = pd.to_datetime(row['Remainder Date']).date()
                        due_date = row['Due Date']
                        amount = row['Amount']

                        # Check if today is the remainder date
                        if remainder_date == today:
                            # Create personalized reminder email content
                            message_body = f"""
                            Hi {name},
                            
                            This is a reminder regarding your upcoming payment:
                            
                            - Remainder Date: {remainder_date}
                            - Due Date: {due_date}
                            - Amount Due: {amount}
                            
                            Please ensure payment is completed by the due date. If you have questions, please contact us.
                            
                            Best regards,
                            [Your Company Name]
                            """

                            # Compose reminder email
                            msg = MIMEMultipart()
                            msg['From'] = FROM_EMAIL
                            msg['To'] = email
                            msg['Subject'] = 'Payment Reminder'
                            msg.attach(MIMEText(message_body, 'plain'))

                            # Send reminder email
                            server.sendmail(FROM_EMAIL, email, msg.as_string())
                            st.success(f'Reminder email sent to {name} ({email}) on the remainder date.')

                    elif row['Has'].strip().lower() == 'yes':
                        # Retrieve details for invoice email
                        name = row['Full name']
                        email = row['Email Address']
                        amount = row['Amount']
                        due_date = row['Due Date']

                        # Create personalized invoice email content
                        invoice_message = f"""
                        Hi {name},
                        
                        Thank you for your payment. Below is the invoice for your records:
                        
                        - Invoice Number: INV-{i+1}
                        - Amount Paid: {amount}
                        - Due Date: {due_date}
                        
                        Thank you for your timely payment!
                        
                        Best regards,
                        [Your Company Name]
                        """

                        # Compose invoice email
                        msg = MIMEMultipart()
                        msg['From'] = FROM_EMAIL
                        msg['To'] = email
                        msg['Subject'] = 'Payment Invoice'
                        msg.attach(MIMEText(invoice_message, 'plain'))

                        # Send invoice email
                        server.sendmail(FROM_EMAIL, email, msg.as_string())
                        st.success(f'Invoice email sent to {name} ({email}).')

                server.quit()
                st.success("All applicable emails sent successfully.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
