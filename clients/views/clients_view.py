from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..models import Client, ClientContact, ClientFile
from django.urls import reverse_lazy, reverse
from mini_erp.forms import AddClientForm
from clients.forms import CreateFileForm, ClientContactForm, ClientForm

class ClientDeleteView(DeleteView):
    model = Client
    template_name= 'general/client_delete.html'
    success_url= reverse_lazy('home')

class ClientContactDeleteView(DeleteView):
    model = ClientContact
    template_name= 'general/client_contact_delete.html'
    success_url= reverse_lazy('home')

class ClientFileDeleteView(DeleteView):
    model = ClientFile
    template_name= 'general/client_file_delete.html'
    success_url= reverse_lazy('home')

class ClientRegisterView(CreateView):
    model = Client
    template_name = 'general/client_add.html'
    success_url= reverse_lazy('home')
    form_class = ClientForm

    def form_valid(self, form):
        return super().form_valid(form)
    
class ClientContactRegisterView(CreateView):
    context_object_name = 'contact'
    model = ClientContact
    template_name = 'general/client_contact_add.html'
    form_class = ClientContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Guardar automáticamente el cliente correspondiente
        form.instance.client_id = self.kwargs["pk"]
        return super().form_valid(form)
    
class ClientFileRegisterView(CreateView):
    context_object_name = 'file'
    model = ClientFile
    template_name = 'general/client_file_add.html'
    form_class = CreateFileForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.client_id = self.kwargs["pk"]
        return super().form_valid(form)

class ClientListView(ListView):
    model= Client
    context_object_name = 'clients'
    template_name = 'general/client_list.html'
    ordering = ["name"]

class ClientDetailView(DetailView):
    model = Client
    template_name= 'general/client_detail.html'
    context_object_name= 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()

        context['contacts'] = client.relacionados.all()
        context['files'] = client.files.all()
        return context
    
class ClientContactDetailView(DetailView):
    model = ClientContact
    template_name = 'general/client_contact_detail.html'
    context_object_name = 'contact'

class ClientFileDetailView(DetailView):
    model = ClientFile
    template_name = 'general/client_file_detail.html'
    context_object_name = 'file'
        
 
class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'general/client_update.html'
    context_object_name = 'update'
    fields = [
        'name',
        'tipo',
        'cif_nif',
        't_number',
        'email',
        'direccion',
        'other',
    ]

    def form_valid(self, form):
        return super(ClientUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clients:clients_detail', args=[self.object.pk])
    
class ClientContactUpdateView(UpdateView):
    model = ClientContact
    template_name = 'general/client_contact_update.html'
    context_object_name = 'update'
    fields = [
        'first_name',
        'last_name',
        'cargo',
        't_number',
        'email',
    ]

    def form_valid(self, form):
        return super(ClientContactUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clients:clients_contact_detail', args=[self.object.pk])
    
