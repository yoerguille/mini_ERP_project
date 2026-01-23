from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import InvoiceCreateView, InvoiceItemCreateView, InvoiceDetailView, InvoiceListView, InvoiceSentEmail, create_pdf
from . import views


app_name = 'invoices'

urlpatterns = [
    path('create/<pk>', InvoiceCreateView.as_view(), name='create_invoice'),
    path('item/create/<pk>', InvoiceItemCreateView.as_view(), name='create_item_invoice'),
    path('detail/<pk>', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),

    path('invoices/send/<pk>', InvoiceSentEmail.as_view(), name='invoice_send_email'),
    path('invoices/pdf/<pk>', views.create_pdf, name='invoice_pdf'),
    
]