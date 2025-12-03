from django.contrib import admin
from .models import Product, ProductVariant

# Register your models here.
class ProductVariantAdmin(admin.TabularInline):
    model= ProductVariant
    extra=1
    classes= ['collapse']
    fields=(
        'color',
        'size',
        'sku',
        'stock',
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = [
        "model",
        'type',
        'sku',
        'allowed_print',
        'image',
        'created_at',
        'updated_at',
    ]

    search_fields=(
        "model",
        'sku',
    )

    list_filter = [
        'allowed_print',
        'type',
        'image',
        'created_at',
        'updated_at',
        ]    
    ordering = [
        "model",
        'sku',
        'allowed_print',
        'image',
        'created_at',
        'updated_at',
        
    ]

    inlines= [
        ProductVariantAdmin,
    ]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "color", "size", "sku", "stock")
    search_fields = ("product__model", "color", "size", "sku")
    list_filter = ("product",)