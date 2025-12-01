from django import forms
from .models import Client, ClientContact, ClientFile

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class ClientContactForm(forms.ModelForm):
    class Meta:
        model = ClientContact
        fields = '__all__'
        widgets = {
            "client": forms.HiddenInput()
        }

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