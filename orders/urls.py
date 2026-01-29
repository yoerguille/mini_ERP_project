from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import OrderDetailView, OrderListView, OrderCreateView, OrderItemCreateView, OrderDeleteView, OrderUpdateView, ChangeStatusView, OrderItemDelete, OrderSentEmail

app_name = 'orders'

urlpatterns = [
    path('list/', OrderListView.as_view(), name='orders'),
    path('detail/<pk>', OrderDetailView.as_view(), name='order_detail'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('update/<pk>', OrderUpdateView.as_view(), name='order_update'),
    path('items_create/<pk>', OrderItemCreateView.as_view(), name='order_item'),
    path('items_delete/<pk>', OrderDeleteView.as_view(), name='order_delete'),
    path('items_items_delete/<pk>', OrderItemDelete.as_view(), name='order_item_delete'),
    path('/status/<pk>', ChangeStatusView.as_view(), name='change_status'),
    path('/email/<pk>', OrderSentEmail.as_view(), name='sent_email'),
]
