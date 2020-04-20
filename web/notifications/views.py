from django.shortcuts import render
from django.conf import settings
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Notification
from .forms import NotificationForm


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = settings.LOGIN_URL
    redirect_field_name = 'redirect_to'

    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    model = Notification

    # def get_queryset(self):
    #     return super().get_queryset().filter(creator=self.request.user)


class NotificationCreate(generic.CreateView):
    form_class = NotificationForm
    template_name = 'notifications/form.html'
    success_url = reverse_lazy('notification-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        return super().form_valid(form)


class NotificationMixin:
    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)


class NotificationEdit(NotificationMixin, generic.UpdateView):
    form_class = NotificationForm
    model = Notification
    template_name = 'notifications/form.html'
    success_url = reverse_lazy('notification-list')

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)


class NotificationDelete(NotificationMixin, generic.DeleteView):
    model = Notification
    success_url = reverse_lazy('notification-list')
