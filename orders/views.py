from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from models import Order

# Create your views here.
class OrderBoardView(TemplateView):
    template_name = 'orders/order_board_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search = self.request.GET.get('q')
        order_by_delivery = self.request.GET.get('order') == 'delivery'

        important_orders = self.Order.objects.filter(order_type='LARGE')
        counter_orders = self.Order.objects.filter(order_type='SMALL')

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
