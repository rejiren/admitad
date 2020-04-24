from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import generic
from .forms import UserRegistrationForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('notification-list')


class UserRegistrationView(generic.CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')


def logout_view(request):
    logout(request)
    return redirect('login')


def index(request):
    return redirect('notification-list')
