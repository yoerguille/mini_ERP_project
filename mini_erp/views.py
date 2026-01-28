from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from orders.models import Order
from django.views.generic import CreateView, FormView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User

class landingView(TemplateView):
    template_name = 'general/landing.html'

class home_view(TemplateView):

    template_name = 'general/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search = self.request.GET.get('q')
        order_by_delivery = self.request.GET.get('order') == 'delivery'

        important_orders = Order.objects.filter(order_type='LARGE')
        counter_orders = Order.objects.filter(order_type='SMALL')

        if search:
            important_orders = important_orders.filter(
                client__name__icontains=search
            )

            counter_orders = counter_orders.filter(
                client__name__icontains=search
            )

        if order_by_delivery:
            important_orders = important_orders.order_by(
                'delivery_date'
            )

            counter_orders = counter_orders.order_by(
                'delivery_date'
            )
        else:
            important_orders = important_orders.order_by(
                '-created_at'
            )

            counter_orders = counter_orders.order_by(
                '-created_at'
            )

        context['important_orders'] = important_orders
        context['counter_orders'] = counter_orders
 
        return context
    
class Login(FormView):
    template_name = 'general/login.html'
    form_class= LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        contraseña = form.cleaned_data.get('password')
        user = authenticate(username=email, password=contraseña)
    
        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f"Bienvenido de nuevo {user.username}")
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.add_message(self.request, messages.ERROR, f"Usuario o contraseña incorrectas")
            return super(Login, self).form_invalid(form)
        
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, f"Cerrado sesión correctamente")
    return HttpResponseRedirect(reverse('home'))

class UserRegisterView(CreateView):
    model = User
    template_name = 'general/register.html'
    success_url= reverse_lazy('login')
    form_class = RegisterForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Usuario creado correctamente")
        return super().form_valid(form)