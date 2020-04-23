from functools import reduce
from datetime import timedelta, datetime
import time
from django.utils import timezone
from celery.task import periodic_task, PeriodicTask
from celery import shared_task
from celery import group, chord
from .emails import send_email
from .models import Notification, ParticipantStatus
from .storage import nearest_notification


@shared_task
def send_mail_task(email, subject, body_text):
    send_email(email, subject, body_text)
    print(email)
    return True


@shared_task
def send_mail_callback(result):
    """
    На случай, если придётся обрабатывать статусы отправки отдельным пользователям
    """
    return result


@shared_task
def process_notification_callback(results, notification_id):
    if reduce((lambda x, y: x & y), results, True):
        Notification.objects.status_success(notification_id)
    else:
        Notification.objects.status_failed(notification_id)
    return results


@periodic_task(run_every=(timedelta(seconds=1)), name='process_notification')
def process_notification():
    if nearest_notification.onset_at < timezone.now():
        notification = nearest_notification.pop()
        job = group(
            [send_mail_task.s(notification.creator.email, notification.title, notification.description)
             | send_mail_callback.s()] +
            [send_mail_task.s(participant.user.email, notification.title, notification.description)
             | send_mail_callback.s()
             for participant in notification.participant_set.filter(status=ParticipantStatus.ACTIVE)]
        ) | process_notification_callback.s(notification.id)
        job.apply_async()
