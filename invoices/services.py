from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO


def generate_invoice_pdf(invoice):
    html_string = render_to_string(
        "invoices/invoice_pdf.html",
        {"invoice": invoice}
    )

    pdf_file = BytesIO()

    HTML(
        string=html_string,
        base_url= None
    ).write_pdf(pdf_file)

    pdf_file.seek(0)
    return pdf_file

def send_invoice_email(invoice):
    html = render_to_string(
        "emails/invoice.html",
        {'invoice':invoice}
    )

    pdf = generate_invoice_pdf(invoice)

    email = EmailMultiAlternatives(
        subject=f"Factura - {invoice.invoice_number}",
        body='Tu cliente no soporta HTML',
        to=[invoice.billing_email]
    )

    email.attach_alternative(html, "text/html")

    email.attach(
        filename=f"Factura_{invoice.invoice_number}.pdf",
        content=pdf.read(),
        mimetype="application/pdf"
    )

    email.send()

