from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Order, OrderItem
from mini_erp.forms import OrderForm, OrderItemForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from invoices.services import send_order_email

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ChangeStatusView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        if new_status in Order.OrderStatus.values:
            order.status = new_status
            order.save()
            

        return redirect('orders:order_detail', order.pk)

@method_decorator(login_required, name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'

@method_decorator(login_required, name='dispatch')
class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'orders/order_update.html'
    fields = [
        'title',
        'status',
        'order_type',
        'notes',
        'delivery_date',
    ]

    def form_valid(self, form):
        return super(OrderUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('orders:order_detail', args=[self.object.pk])
    
class OrderItemDelete(DeleteView):
    model = OrderItem
    template_name = 'orders/order_item_delete.html'

    def get_success_url(self):
        return reverse('orders:order_detail', args=[self.object.order.pk])

@method_decorator(login_required, name='dispatch')
class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order_delete.html'
    success_url = reverse_lazy('orders:orders')

@method_decorator(login_required, name='dispatch')
class OrderItemCreateView(CreateView):
    model = OrderItemForm
    template_name = 'orders/order_item.html'
    form_class = OrderItemForm
    success_url = reverse_lazy('orders:orders')

    def form_valid(self, form):
        order = Order.objects.get(pk=self.kwargs['pk'])

        item = form.save(commit=False)
        item.order = order
        item.save()

        messages.add_message(self.request, messages.SUCCESS, f"¡{item} añadido exitosamente al encargo!")

        return redirect('orders:order_item', order.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(pk=self.kwargs['pk'])
        context["order"] = order
        context["items"] = order.items.all()
        return context
    
    
    
    
@method_decorator(login_required, name='dispatch')
class OrderCreateView(CreateView):
    model = Order
    template_name = 'orders/order_create.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse('orders:order_item', args=[self.object.pk])

@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'orders/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = Order.objects.select_related('client')
        search = self.request.GET.get('q')
        if search:
            qs = qs.filter(title__icontains = search)

        client = self.request.GET.get('client')
        if client:
            qs = qs.filter(client__id=client)

        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)

        created_from = self.request.GET.get('created_from')
        if created_from:
            qs = qs.filter(created_at__date__gte=created_from)

        created_to = self.request.GET.get('created_to')
        if created_to:
            qs= qs.filter(created_at__date__lte=created_to)

        delivery_from = self.request.GET.get('delivery_from')
        if delivery_from:
            qs = qs.filter(delivery_date__gte=delivery_from)

        delivery_to = self.request.GET.get("delivery_to")
        if delivery_to :
            qs = qs.filter(delivery_date__lte=delivery_to)

        return qs.order_by("-created_at")


    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["clients"] = Order._meta.get_field("client").remote_field.model.objects.all()
        context['status'] = Order.OrderStatus.choices
 
        return context
    
class OrderSentEmail(View):
    def post(self, request, pk ):
        order = get_object_or_404(Order, pk=pk)

        if order.sent_at:
            messages.warning(request, "El aviso al cliente ya fue enviado anteriormente.")
            return redirect('orders:order_detail', order.pk)

        send_order_email(order)
        order.sent_at = timezone.now()
        order.status = Order.OrderStatus.COMPLETED
        order.save()

        messages.success(request, 'Aviso a Cliente enviado con éxito')

        return redirect('orders:order_detail', order.pk)



    
    

    
