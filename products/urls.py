from django.contrib import admin
from django.urls import path, include
from .views import ProductCatalogView, ProductDetail

app_name = "products"

urlpatterns = [
    path('catalog/', ProductCatalogView.as_view(), name='products_catalog'),
    path('catalog/<pk>', ProductDetail.as_view(), name='product_detail'),
]
