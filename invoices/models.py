from django.db import models
from orders.models import Order
from decimal import Decimal, ROUND_HALF_UP

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
    billing_email = models.EmailField(blank=True)

    invoice_number = models.CharField(
        max_length=30,
        unique=True,
    )
    issue_date = models.DateField()
    due_date = models.DateField(
        null=True,
        blank=True,
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
    
    def base_amount(self):
        return sum(
            item.unit_price * item.quantity 
            for item in self.items.all()
        )
    
    def vat_amount(self):
        return (self.base_amount() * Decimal(0.21)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
    
    def total_with_vat(self):
        return(self.base_amount() + self.vat_amount())
    
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

    def total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.description}"
    
