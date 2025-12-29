from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from clients.models import Client
from orders.models import Order, OrderItem

class AddClientForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model= Client
        fields = [
            'name',
            'tipo',
            'cif_nif',
            't_number',
            'email',
            'direccion',
            'other',   
        ]

    def save(self, commit= True):
        client = super().save(commit=True)
        client.save()

class LoginForm(forms.Form):
    username= forms.CharField(label='Usuario')
    password=forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'client',
            'title',
            'status',
            'order_type',
            'notes',
            'delivery_date',
        ]

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = [
            'order',
            'product',
            'variant',
            'quantity',
            'unit_price',
            'notes',
        ]

class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model= User
        fields = [
            'first_name',
            'username',
            'email',
            'password',   
        ]

    def save(self, commit= True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password'])
        user.save()

        return user