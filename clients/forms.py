from django import forms
from .models import Client, ClientContact, ClientFile

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields =[ 'name',
            'tipo',
            'cif_nif',
            't_number',
            'email',
            'direccion',
            'other',
        ]

class ClientContactForm(forms.ModelForm):
    class Meta:
        model = ClientContact
        fields = [
            'first_name',
            'last_name',
            'cargo',
            't_number',
            'email',
        ]

class ClientFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = '__all__'
        widgets = {
            "client": forms.HiddenInput()
        }

class CreateFileForm(forms.ModelForm):
    class Meta:
        model= ClientFile
        fields = [
            'file',
            'descripcion',
            'created_at',  
        ]