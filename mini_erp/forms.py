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