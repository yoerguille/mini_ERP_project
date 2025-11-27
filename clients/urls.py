
from django.contrib import admin
from django.urls import path, include
from .views.clients_view import ClientListView, ClientDetailView, ClientUpdateView, ClientContactDetailView, ClientContactUpdateView
from .views.clients_view import ClientRegisterView

app_name = "clients"

urlpatterns = [
    path('list/', ClientListView.as_view(), name='clients_list'),
    path('add/', ClientRegisterView.as_view(), name='clients_add'),
    path('detail/<pk>', ClientDetailView.as_view(), name='clients_detail'),
    path('update/<pk>', ClientUpdateView.as_view(), name='clients_update'),
    path('contact/detail/<pk>', ClientContactDetailView.as_view(), name='clients_contact_detail'),
    path('contact/update/<pk>', ClientContactUpdateView.as_view(), name='clients_contact_update'),

]
