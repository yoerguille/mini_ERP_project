from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Order, OrderItem
from mini_erp.forms import OrderForm, OrderItemForm
from django.urls import reverse_lazy, reverse

# Create your views here.
class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'

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

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order_delete.html'
    success_url = reverse_lazy('orders:orders')

class OrderItemCreateView(CreateView):
    model = OrderItemForm
    template_name = 'orders/order_item.html'
    form_class = OrderItemForm
    success_url = reverse_lazy('orders:orders')

class OrderCreateView(CreateView):
    model = Order
    template_name = 'orders/order_create.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse('orders:order_item', args=[self.object.pk])

class OrderListView(ListView):
    model = Order
    template_name = 'orders/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search = self.request.GET.get('q')
        order_by_delivery = self.request.GET.get('order') == 'delivery'

        important_orders = Order.objects.filter(order_type='LARGE')
        counter_orders = Order.objects.filter(order_type='SMALL')

        if search:
            important_orders = important_orders.filter(
                client__name__icontains=search
            )

            counter_orders = counter_orders.filter(
                client__name__icontains=search
            )

        if order_by_delivery:
            important_orders = important_orders.order_by(
                'delivery_date'
            )

            counter_orders = counter_orders.order_by(
                'delivery_date'
            )
        else:
            important_orders = important_orders.order_by(
                '-created_at'
            )

            counter_orders = counter_orders.order_by(
                '-created_at'
            )

        context['important_orders'] = important_orders
        context['counter_orders'] = counter_orders
 
        return context
    
    

    
