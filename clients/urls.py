
from django.contrib import admin
from django.urls import path, include
from .views.clients_view import ClientListView, ClientDetailView

app_name = "clients"

urlpatterns = [
    path('list/', ClientListView.as_view(), name='clients_list'),
    path('detail/<pk>', ClientDetailView.as_view(), name='clients_detail'),

]
