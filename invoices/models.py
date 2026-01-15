from django.db import models
from orders.models import Order

# Create your models here.

class Invoices(models.Model):
    class InvoiceStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Borrador'
        ISSUED = 'ISSUED', 'Emitida'
        PAID = 'PAID', 'Pagada'
        CANCELLED = 'CANCELLED', 'Cancelada'

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name= 'invoices'
    )

    client_name = models.CharField(max_length=150)
    cifnif = models.CharField(max_length=20)
    client_adress = models.CharField(max_length=150)

    invoice_number = models.CharField(
        max_length=30,
        unique=True,
    )
    issue_date = models.DateField()
    due_date = models.DateField(
        null=True,
        blank=True,
    )

    base_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Base imponible'
    )

    vat_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='IVA total'
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Importe total'
    )

    status = models.CharField(
        verbose_name='Estado',
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.DRAFT,

    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Factura - {self.invoice_number}"
    
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoices,
        on_delete=models.CASCADE,
        related_name='items'
    )

    description = models.CharField(
        help_text='Concepto facturado',
        max_length=255,
    )

    quantity = models.PositiveIntegerField()

    unit_price= models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Precio unitario sin IVA'
    )

    line_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Total de la linea'
    )

    def __str__(self):
        return f"{self.quantity} x {self.description}"