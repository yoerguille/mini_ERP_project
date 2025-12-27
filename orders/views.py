from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Order, OrderItem

# Create your views here.
class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'

    

    
