from django.contrib import admin
from .models import Order, OrderItem, OrderDesignFile

# Register your models here.
class OrderDesignFileAdmin(admin.TabularInline):
    model = OrderDesignFile
    extra = 1
    classes = ['collapse']
    fields =(
        'file',
        'description'
    )

class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 1
    classes = ['collapse']
    fields = (
        'product',
        'variant',
        'quantity',
        'unit_price',
        'notes',
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        "client",
        'title',
        'status',
        'order_type',
        'delivery_date',
    ]
    readonly_fields= (
        'created_at',
        'updated_at',
    )

    search_fields=(
        "client",
        'title',
    )

    list_filter = [
        'client',
        'status',
        'order_type',
        'created_at',
        ]  
      
    ordering = [
        'status',
        'order_type',
        'created_at',
        
    ]

    inlines= [
        OrderDesignFileAdmin,
        OrderItemAdmin
    ]