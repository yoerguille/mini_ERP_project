from django.contrib import admin
from .models import Invoices, InvoiceItem

# Register your models here.

class InvoiceItemAdmin(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    classes = ['collapse']
    fields = (
        'invoice',
        'description',
        'quantity',
        'unit_price',
    )

@admin.register(Invoices)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = [
        'order',
        'client_name',
        'cifnif',
        'client_adress',
        'billing_email',
        'invoice_number',
        'issue_date',
        'due_date',
        'status',
        'created_at'
    ]
    readonly_fields= (
        'client_name',
        'cifnif',
        'client_adress',
        'billing_email',
        'invoice_number',
        'issue_date',
        'due_date',
        'status',
        'created_at'
    )

    search_fields=(
        'client_name',
        'cifnif',
        'client_adress',
        'billing_email',
        'invoice_number',
        'issue_date',
    )

    list_filter = [
        'client_name',
        'status',
        ]  
      
    ordering = [
        'invoice_number',
        'issue_date',
        
    ]

    inlines= [
        InvoiceItemAdmin
    ]
