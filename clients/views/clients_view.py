from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..models import Client
from django.urls import reverse_lazy, reverse

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