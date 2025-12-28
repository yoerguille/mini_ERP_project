from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from clients.models import Client

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