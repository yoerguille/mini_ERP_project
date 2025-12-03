from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, ProductVariant

# Create your views here.
class ProductCatalogView(ListView):
    model= Product
    template_name = 'products/products_catalog.html'
    ordering = ["model"]
    context_object_name = 'products'