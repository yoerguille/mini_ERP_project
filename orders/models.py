from django.db import models
from clients.models import Client
from products.models import Product, ProductVariant
from decimal import Decimal, ROUND_HALF_UP

# Create your models here.
class Order(models.Model):
    class OrderStatus(models.TextChoices):
        RECEIVED = "RECEIVED", "Recibido"
        PENDING_DESIGN = "PENDING_DESIGN", "Pendiente de diseño"
        DESIGN_READY = "DESIGN_READY", "Diseño confirmado"
        IN_PRODUCTION = "IN_PRODUCTION", "En producción"
        COMPLETED = "COMPLETED", "Completado"
        DELIVERED = "DELIVERED", "Entregado"
        CANCELLED = "CANCELLED", "Cancelado"

    class OrderType(models.TextChoices):
        LARGE = 'LARGE', 'Encargo Importante'
        SMALL = 'SMALL', 'Encargo de Mostrador'

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='orders',  
    )

    title = models.CharField(
        max_length=50,
        help_text='Descripcion corta del Pedido',
        verbose_name='Nombre',
    )

    status = models.CharField(
        verbose_name='Estado',
        choices=OrderStatus,
        default=OrderStatus.PENDING_DESIGN,

    )

    order_type =models.CharField(
        verbose_name='Tipo de pedido',
        choices=OrderType,
    )

    notes = models.TextField(blank=True, null=True)

    delivery_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sent_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.pk} - {self.client.name} "
    
    def total_price(self):
        return sum(
            item.unit_price * item.quantity 
            for item in self.items.all()
        )
    
    def total_price_with_vat(self):
        return (self.total_price() * Decimal(1.21)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
    
    def status_color(self):
        return {
            self.OrderStatus.RECEIVED: 'secondary',
            self.OrderStatus.PENDING_DESIGN: 'warning',
            self.OrderStatus.DESIGN_READY: 'info',
            self.OrderStatus.IN_PRODUCTION: 'primary',
            self.OrderStatus.COMPLETED: 'success',
            self.OrderStatus.DELIVERED: 'dark',
            self.OrderStatus.CANCELLED: 'danger',
        }.get(self.status, 'secondary')

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField(
        default=1,
        
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Precio unitario sin IVA",
        verbose_name='Precio presupuestado',
    )

    notes = models.CharField(
        max_length=255,
        blank=True,
    )

    def total_price(self):
        return self.unit_price * self.quantity
    
    def total_price_with_vat(self, vat=0.21):
        return self.total_price() * (1+vat)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.model}"
    
class OrderDesignFile(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="design_files",
    )

    file = models.FileField(upload_to="orders/designs/")
    description = models.CharField(max_length=200, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diseño Pedido #{self.order.pk}"