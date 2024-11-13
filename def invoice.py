def generate_invoice_pdf(data, invoice_number):
    """Generate a PDF invoice dynamically based on provided data."""
    pdf_path = f"Invoice_{invoice_number}.pdf"
    
    # Set up the document and canvas
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter  # Get the dimensions of the page
    
    # Add Company Logo
    logo_path = "logo.png"  # Replace with your actual logo path
    c.drawImage(logo_path, 30, height - 80, width=250, height=250)
    
    # Add Company Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(150, height - 50, "ARCHER WEBSOL")
    c.setFont("Helvetica", 10)
    c.drawString(150, height - 65, "GSTIN: 33ANPPP0425L2ZS")
    c.drawString(150, height - 80, "support@archerwebsol.com | www.archerwebsol.com | 8056109699 | 9790740735")

    # Invoice Title and Ref Number
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 120, "INVOICE")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 135, f"Ref Number: {data['Bill Number']}")
    c.drawString(40, height - 150, f"Bill Date: {data['Bill Date'].date() if isinstance(data['Bill Date'], datetime) else data['Bill Date']}")

    # Add Invoice Details
    invoice_details = [
        ['Invoice Number:', invoice_number],
        ['Invoice Date:', f"{data['Invoice Date'].date() if isinstance(data['Invoice Date'], datetime) else data['Invoice Date']}"],
        ['Website URL:', data['Website url']],
        ['Date of Order:', f"{data['Date Order'].date() if isinstance(data['Date Order'], datetime) else data['Date Order']}"],
        ['Date of Registration:', f"{data['Date Registration'].date() if isinstance(data['Date Registration'], datetime) else data['Date Registration']}"],
    ]
    
    invoice_table = Table(invoice_details, colWidths=[200, 300])
    invoice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    
    invoice_table.wrapOn(c, 40, height - 170)
    invoice_table.drawOn(c, 40, height - 200)

    # Add Client Information
    client_info = [
        ['Client Name:', data['Company Name']],
        ['Place of Client:', data['Place Client']],
        ['State:', data['State']],
        ['Pincode:', data['Pincode']],
        ['GSTIN:', data['GST Number']],
        ['Address:', f"{data['Address City/District']}, {data['State']}, {data['Pincode']}"],
        ['Proforma Date:', f"{data['Proforma Date'].date() if isinstance(data['Proforma Date'], datetime) else data['Proforma Date']}"]
    ]

    client_table = Table(client_info, colWidths=[200, 300])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))

    client_table.wrapOn(c, 40, height - 340)
    client_table.drawOn(c, 40, height - 370)

    # Product Table
    product_details = [
        ['S.No', 'Product Description', 'Period', 'Amount', 'CGST Rate', 'CGST Amt', 'SGST Rate', 'SGST Amt', 'Total'],
        ['1', data['Item Description'], data['Period'], f"{data['Net Amount']}", f"{data['CGST Percent']}%", f"{data['CGST Amount']}", f"{data['SGST Percent']}%", f"{data['SGST Amount']}", f"{data['Gross Amount']}"]
    ]
    
    product_table = Table(product_details, colWidths=[30, 120, 60, 60, 60, 60, 60, 60, 60])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    product_table.wrapOn(c, 40, height - 420)
    product_table.drawOn(c, 40, height - 450)

    # Total Amount Section
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, 150, f"Total Amount Before Tax: {data['Net Amount']}")
    c.drawString(40, 135, f"Total Tax Amount: {data['IGST Amount'] + data['CGST Amount'] + data['SGST Amount']}")
    c.drawString(40, 120, f"Total Amount After Tax: {data['Gross Amount']}")
    c.drawString(40, 105, f"Round Off: {data['Gross Amount']}")

    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(40, 80, "Thanking you and assuring our best services to you at all times.")

    # Save PDF
    c.save()
    return pdf_path

                        # Generate PDF invoice
                        pdf_path = generate_invoice_pdf(data, invoice_number)
                        with open(pdf_path, 'rb') as pdf_file:
                            pdf = MIMEApplication(pdf_file.read(), _subtype="pdf")
                            pdf.add_header('Content-Disposition', 'attachment', filename=f'Invoice_{invoice_number}.pdf')
                            msg.attach(pdf)

                        # Send email
                        server.sendmail(FROM_EMAIL, email, msg.as_string())
                        st.success(f'Invoice email sent to {data["Contact Person"]} ({email}).')

                        # Clean up generated PDF
                        os.remove(pdf_path)