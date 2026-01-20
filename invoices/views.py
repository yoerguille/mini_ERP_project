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
from orders.models import Order, OrderItem
from django.utils.timezone import now
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta

# Create your views here.

@method_decorator(login_required, name='dispatch')
class InvoiceListView(ListView):
    model = Invoices
    template_name = 'invoices/invoices_list.html'
    context_object_name = 'invoices'
    

class InvoiceDetailView(DetailView):
    model = Invoices
    template_name = 'invoices/invoice_detail.html'



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
    
 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(pk=self.kwargs['pk'])
        context["order"] = order
        context["items"] = order.items.all()
        return context
    
    def create_invoice_number(self):
        year = now().year

        last_invoice = (Invoices.objects.filter(
            invoice_number__startswith=str(year))
            .order_by("-invoice_number")
            .first()
        )

        if last_invoice and last_invoice.invoice_number:
            last_number = int(last_invoice.invoice_number.split("-")[1])
        else:
            last_number = 0

        new_number = last_number + 1

        return f"{year}-{new_number:05d}"

    def get_due_date(self):
        today = date.today()
        due_date = today + timedelta(days=30)

        return due_date

    
    def get_initial(self):
        initial = super().get_initial()
        order = Order.objects.get(pk=self.kwargs['pk'])
        client = order.client
        n_invoice = self.create_invoice_number()

        initial['client_name'] = client.name
        initial['cifnif'] = client.cif_nif
        initial['client_adress'] = client.direccion
        initial['billing_email'] = client.email
        initial['invoice_number'] = n_invoice
        initial['issue_date'] = date.today()
        initial['due_date'] = self.get_due_date()

        return initial
    
    
    
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

