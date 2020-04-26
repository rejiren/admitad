from functools import reduce
from datetime import timedelta

from celery.task import periodic_task
from celery import shared_task, group
from django.utils import timezone

from .emails import send_email, get_notification_body
from .models import Notification, ParticipantStatus
from .storage import nearest_notification


@shared_task
def send_mail_task(email, subject, body):
    send_email(email, subject, body)
    return True


@shared_task
def send_mail_callback(result):
    """
    На случай, если придётся обрабатывать статусы отправки для отдельных пользователей
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
    if nearest_notification.pk and nearest_notification.onset_at < timezone.now():
        notification = nearest_notification.pop()
        participants_emails = [
            participant.user.email for participant in
            notification.participant_set.filter(status=ParticipantStatus.ACTIVE)
            if participant.status
        ]
        participants_emails.append(notification.creator.email)

        body_text = get_notification_body(
            notification.place,
            notification.description,
            participants_emails,
            notification.onset_at,
            notification.created_at,
        )
        job = group([
            send_mail_task.s(email, notification.title, body_text) | send_mail_callback.s()
            for email in participants_emails
        ]) | process_notification_callback.s(notification.id)
        job.apply_async()
