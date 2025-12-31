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

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ChangeStatusView(View):
    def post(self, request, pk, status):
        order = get_object_or_404(Order, pk=pk)
        order.status = status
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
    
    

    
