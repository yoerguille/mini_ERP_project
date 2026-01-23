from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_invoice_email(invoice):
    html = render_to_string(
        "emails/invoice.html",
        {'invoice':invoice}
    )

    email = EmailMultiAlternatives(
        subject=f"Factura - {invoice.invoice_number}",
        body='Tu cliente no soporta HTML',
        to=[invoice.billing_email]
    )

    email.attach_alternative(html, "text/html")
    email.send()