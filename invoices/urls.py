from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import InvoiceCreateView


app_name = 'invoices'

urlpatterns = [
    path('create/<pk>', InvoiceCreateView.as_view(), name='create_invoice'),
    
]