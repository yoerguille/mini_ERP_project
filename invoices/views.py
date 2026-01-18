from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from mini_erp.forms import OrderForm, OrderItemForm, InvoiceForm, InvoiceItemForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Invoices, InvoiceItem
from orders.models import Order

# Create your views here.

class InvoiceCreateView(CreateView):
    model = Invoices
    template_name = 'invoices/create_invoice.html'
    form_class = InvoiceForm

    def get_success_url(self):

        return reverse('invoices:create_item_invoice', args=[self.object.pk])
    
    def form_valid(self, form):
        order = Order.objects.get(pk=self.kwargs['pk'])

        invoice = form.save(commit=False)
        invoice.order = order
        invoice.save()

        messages.add_message(self.request, messages.SUCCESS, f"¡{invoice} añadido exitosamente al encargo!")

        return redirect('invoices:create_item_invoice', invoice.pk)
    
    def get_initial(self):
        initial = super().get_initial()
        order = Order.objects.get(pk=self.kwargs['pk'])
        client = order.client

        initial['client_name'] = client.name
        initial['cifnif'] = client.cif_nif
        initial['client_adress'] = client.direccion
        initial['billing_email'] = client.email
        

        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(pk=self.kwargs['pk'])
        context["order"] = order
        context["items"] = order.items.all()
        return context
    
@method_decorator(login_required, name='dispatch')
class InvoiceItemCreateView(CreateView):
    model = InvoiceItem
    template_name = 'invoices/invoice_item_create.html'
    form_class = InvoiceItemForm
    success_url = reverse_lazy('orders:orders')

    def form_valid(self, form):
        invoice = Invoices.objects.get(pk=self.kwargs['pk'])

        invoice_item = form.save(commit=False)
        invoice_item.invoice = invoice
        invoice_item.save()

        messages.add_message(self.request, messages.SUCCESS, f"¡{invoice_item} añadido exitosamente a la factura!")

        return redirect('invoices:create_item_invoice', invoice.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = Invoices.objects.get(pk=self.kwargs['pk'])
        order = invoice.order
        context["invoice"] = invoice
        context["invoice_items"] = invoice.items.all()
        context['items'] = invoice.order.items.all()
        context['order'] = order
        return context

