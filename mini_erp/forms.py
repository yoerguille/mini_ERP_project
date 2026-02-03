from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from clients.models import Client
from orders.models import Order, OrderItem
from invoices.models import Invoices, InvoiceItem

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

        widgets = {
            'delivery_date' : forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            )
        }
        

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoices

        fields = [
            'client_name',
            'cifnif',
            'client_adress',
            'billing_email',
            'invoice_number',
            'issue_date',
            'due_date',
            'status',
        ]

        widgets = {
            'issue_date' : forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'due_date' : forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            )
        }

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = {
            'description',
            'quantity',
            'unit_price',
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = [
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