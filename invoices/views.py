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
from clients.models import Client
from django.db.models import Q
from django.core.mail import send_mail
from django.utils import timezone
from .services import send_invoice_email, generate_invoice_pdf
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO
from mini_erp import settings

# Create your views here.

@method_decorator(login_required, name='dispatch')
class InvoiceListView(ListView):
    model = Invoices
    template_name = 'invoices/invoices_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        qs = Invoices.objects.select_related('order')
        search = self.request.GET.get('q')
        ordenar = self.request.GET.get('ordenar')
        date = self.request.GET.get('date')

        if search:
            qs = qs.filter( 
                Q(order__title__icontains = search) |
                Q(client_name__icontains = search)
            )
        
        if date == 'issue_date':
            qs = qs.order_by('issue_date')

        if date == '-issue_date':
            qs = qs.order_by('-issue_date')
        
        if ordenar == 'invoice_number':
            qs = qs.order_by('invoice_number')
        if ordenar == '-invoice_number':
            qs = qs.order_by('-invoice_number')

        client = self.request.GET.get('client')
        if client:
            qs = qs.filter(client__id=client)

        issue_date_from = self.request.GET.get('issue_from')
        if issue_date_from:
            qs = qs.filter(issue_date__gte=issue_date_from)

        issue_date_to = self.request.GET.get('issue_to')
        if issue_date_to:
            qs = qs.filter(issue_date__lte=issue_date_to)

        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['status'] = Invoices.InvoiceStatus.choices

        return context
    
class InvoicePDFDownload(View):
    def get(self, request, pk):
        invoice= get_object_or_404(Invoices, pk=pk)

        pdf_file = generate_invoice_pdf(invoice)

        response = HttpResponse(
            pdf_file.read(),
            content_type='application/pdf'
        )

        response["Content-Disposition"] = (
            f'inline; filename="Factura_{invoice.invoice_number}.pdf"'
        )

        return response
    
class InvoiceDelete(DeleteView):
    model = Invoices
    template_name = 'invoices/invoice_delete.html'

    def get_success_url(self):
        return reverse('invoices:invoice_list')



class InvoiceSentEmail(View):

    def post(self, request, pk):
        invoice = get_object_or_404(Invoices, pk=pk)

        if invoice.sent_at:
            messages.warning(request, "La factura ya fue enviada")
            return redirect("invoices:invoice_detail", invoice.pk)

        send_invoice_email(invoice)

        invoice.sent_at = timezone.now()
        invoice.status = Invoices.InvoiceStatus.ISSUED
        invoice.save()

        messages.success(request, "Factura enviada correctamente")

        return redirect('invoices:invoice_detail', invoice.pk)
    

class InvoiceDetailView(DetailView):
    model = Invoices
    template_name = 'invoices/invoice_detail.html'


class InvoiceUpdateView(UpdateView):
    model = Invoices
    template_name = 'invoices/invoice_update.html'
    fields = [
        'client_name',
        'cifnif',
        'client_adress',
        'billing_email',
        'invoice_number',
        'issue_date',
        'due_date',
    ]

    def form_valid(self, form):
        return super(InvoiceUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('invoices:invoice_detail', args=[self.object.pk])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = Invoices.objects.get(pk=self.kwargs['pk'])
        order = invoice.order
        context["order"] = order
        context["items"] = order.items.all()
        return context


class InvoiceDraftView(View):

    def get(self, request, pk):
        invoice = get_object_or_404(Invoices, pk=pk)

        form = InvoiceItemForm

        return render(request, "invoices/invoice_draft.html", {
            "invoice": invoice,
            "order": invoice.order,
            "items": invoice.order.items.all(),
            "invoice_items": invoice.items.all(),
            "form": InvoiceItemForm(),
        })
    
    def post(self, request, pk):
        invoice = get_object_or_404(Invoices, pk=pk)

        if invoice.status != Invoices.InvoiceStatus.DRAFT:
            messages.add_message(self.request, messages.ERROR, f"¡No se puede editar una factura ya emitida!")
            return redirect('invoices:invoice_detail', invoice.pk)
        
        action = request.POST.get("action")

        if action == 'add':
            form = InvoiceItemForm(request.POST)
            if form.is_valid(): 
                item = form.save(commit=False)
                item.invoice = invoice
                item.save()

        elif action == 'delete':
            item_id = request.POST.get('item_id')
            InvoiceItem.objects.filter(
                pk = item_id,
                invoice = invoice
            ).delete()
        
        return redirect('invoices:invoice_draft', invoice.pk)
        

class InvoiceCreateView(CreateView):
    model = Invoices
    template_name = 'invoices/create_invoice.html'
    form_class = InvoiceForm

    
    def form_valid(self, form):
        order = Order.objects.get(pk=self.kwargs['pk'])

        invoice = form.save(commit=False)
        invoice.order = order
        invoice.save()

        messages.add_message(self.request, messages.SUCCESS, f"¡{invoice} añadido exitosamente al encargo!")

        return redirect('invoices:invoice_detail', invoice.pk)
    
 
    
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
    

    


