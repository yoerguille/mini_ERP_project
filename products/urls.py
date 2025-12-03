from django.contrib import admin
from django.urls import path, include
from .views import ProductCatalogView

app_name = "products"

urlpatterns = [
    path('catalog/', ProductCatalogView.as_view(), name='products_catalog')
]
