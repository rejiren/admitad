from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Notification
from .forms import NotificationForm


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = settings.LOGIN_URL
    redirect_field_name = 'redirect_to'

    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    model = Notification

    def get_queryset(self):
        return self.model.objects.order_by('-onset_at').prefetch_related('participants').filter(
            Q(participant__user=self.request.user) | Q(creator=self.request.user)
        ).distinct()


class NotificationCreate(LoginRequiredMixin, generic.CreateView):
    form_class = NotificationForm
    template_name = 'notifications/form.html'
    success_url = reverse_lazy('notification-list')
    login_url = settings.LOGIN_URL

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class NotificationMixin:
    model = Notification

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)


class NotificationEdit(NotificationMixin, LoginRequiredMixin, generic.UpdateView):
    login_url = settings.LOGIN_URL
    form_class = NotificationForm
    template_name = 'notifications/form.html'
    success_url = reverse_lazy('notification-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class NotificationDelete(NotificationMixin, LoginRequiredMixin, generic.DeleteView):
    login_url = settings.LOGIN_URL
    template_name = 'notifications/delete_confirm.html'
    success_url = reverse_lazy('notification-list')
