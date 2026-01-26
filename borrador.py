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