from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, ProductVariant
from decimal import Decimal

# Create your views here.
class ProductCatalogView(ListView):
    model= Product
    template_name = 'products/products_catalog.html'
    ordering = ["model"]
    context_object_name = 'products'

    
    

class ProductDetail(DetailView):
    model = Product
    template_name = 'products/products_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["price_20"] = product.price_20() 
        context["price_25"] = product.price_25()

        margin = self.request.GET.get('margin')
        if margin:
            try:

                margin = float(margin)
                context['custom_price'] =round(product.cost_price * Decimal((1 + margin/100)), 2)
                context['custom_margin'] = margin

            except ValueError:
                context['custom_price'] = None
                context['custom_margin'] = None
                
        return context


    