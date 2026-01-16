from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from mini_erp.forms import OrderForm, OrderItemForm, InvoiceForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Invoices
from orders.models import Order

# Create your views here.

class InvoiceCreateView(CreateView):
    model = Invoices
    template_name = 'invoices/create_invoice.html'
    form_class = InvoiceForm

    def get_success_url(self):
        return reverse('orders:orders')
    
    def form_valid(self, form):
        order = Order.objects.get(pk=self.kwargs['pk'])

        invoice = form.save(commit=False)
        invoice.order = order
        invoice.save()

        messages.add_message(self.request, messages.SUCCESS, f"¡{invoice} añadido exitosamente al encargo!")

        return redirect('orders:orders')
    
    def get_initial(self):
        initial = super().get_initial()
        order = Order.objects.get(pk=self.kwargs['pk'])
        client = order.client

        initial['client_name'] = client.name
        initial['cifnif'] = client.cif_nif
        initial['client_adress'] = client.direccion
        initial['billing_email'] = client.email

        return initial

