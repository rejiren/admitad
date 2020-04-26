from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from .models import Notification, Participant, ParticipantStatus
from .forms import NotificationForm


class NotificationLoginRequiredMixin(LoginRequiredMixin):
    login_url = settings.LOGIN_URL


class IndexView(NotificationLoginRequiredMixin, generic.ListView):
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    model = Notification

    def get_queryset(self):
        return self.model.objects.order_by('-onset_at').prefetch_related('participants').filter(
            Q(participant__user=self.request.user) | Q(creator=self.request.user)
        ).distinct()


class NotificationCreate(NotificationLoginRequiredMixin, generic.CreateView):
    form_class = NotificationForm
    template_name = 'notifications/form.html'
    success_url = reverse_lazy('notification-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['creator'] = self.request.user
        return initial


class NotificationEdit(NotificationLoginRequiredMixin, generic.UpdateView):
    form_class = NotificationForm
    template_name = 'notifications/form.html'
    success_url = reverse_lazy('notification-list')
    model = Notification

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)

    def get_initial(self):
        initial = super().get_initial()
        initial['creator'] = self.request.user
        return initial


class NotificationDelete(NotificationLoginRequiredMixin, generic.DeleteView):
    template_name = 'notifications/delete_confirm.html'
    success_url = reverse_lazy('notification-list')
    model = Notification

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)


class ChangeParticipantStatusView(NotificationLoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = 'notification-list'

    def get(self, *args, **kwargs):
        participant = get_object_or_404(Participant, pk=kwargs.pop('pk'), user=self.request.user)
        participant.status = ParticipantStatus.REJECTED if participant.status else ParticipantStatus.ACTIVE
        participant.save()
        return super().get(*args, **kwargs)
