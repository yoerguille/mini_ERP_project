from django.db import models
from decimal import Decimal

# Create your models here.
class Product(models.Model):
    class PrintType(models.TextChoices):
        DTF = "DTF", "DTF"
        NONE = "NONE", "Sin personalización"

    class ClotheType(models.TextChoices):
        TSHIRT = "TSHIRT", "Camiseta"
        HOODIE = "HOODIE", "Sudadera"
        PANTS = "PANTS", "Pantalón"
        OTHER = "OTHER", "Otros"

    model = models.CharField(
        verbose_name= 'Modelo del Producto',
        max_length=100,
        unique=True
    )

    sku = models.CharField(
        max_length=50,
        blank=True,
        help_text="Referencia interna (opcional)",
    )

    allowed_print = models.CharField(
        max_length=10,
        choices=PrintType.choices,
        default=PrintType.DTF
    )

    type = models.CharField(
        max_length=20,
        choices=ClotheType.choices,
    )

    image = models.ImageField(
        upload_to='products/products_files',
        blank=True,
        null=True,
    )

    model_url = models.URLField(
        blank=True,
        null= True,
    )

    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["model"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        parts = [self.type]
        parts.append(self.model)
        return " - ".join(parts)
    
    def price_20(self):
        return round(self.cost_price * Decimal(1.20), 2)
    
    def price_25(self):
        return round(self.cost_price * Decimal(1.25), 2)


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    color = models.CharField(
        max_length=60,

    )

    size = models.CharField(
        max_length=30,  
    )

    sku = models.CharField(
        max_length=50,
        blank=True,
        help_text="Referencia interna (opcional)",
    )

    stock = models.IntegerField(default=0, help_text="Stock opcional por variante")

    class Meta:
        unique_together = ("product", "color", "size")
        ordering = ["product", "color", "size"]
        verbose_name = "Variante de Producto"
        verbose_name_plural = "Variantes de Producto"

    def __str__(self):
        parts = [self.product.model]
        if self.color:
            parts.append(self.color)
        if self.size:
            parts.append(self.size)
        return " - ".join(parts)