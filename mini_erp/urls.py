
from django.contrib import admin
from django.urls import path, include
from .views import home_view
from django.conf import settings
from django.conf.urls.static import static
from .views import Login, logout_view, UserRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path("logout/", logout_view, name='logout'),
    path("register/", UserRegisterView.as_view(), name='register'),

    path("clients/", include('clients.urls', namespace='clients')),
    path("products/", include('products.urls', namespace='products')),
    path("orders/", include('orders.urls', namespace='orders')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
