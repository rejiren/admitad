from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models


class NotificationStatus(models.IntegerChoices):
    ACTIVE = 1
    IN_PROGRESS = 2
    SUCCESS = 3
    FAILED = 4


class ParticipantStatus(models.IntegerChoices):
    ACTIVE = 1
    REJECTED = 0


class NotificationManager(models.Manager):
    def nearest(self):
        return self.filter(status=NotificationStatus.ACTIVE).order_by('onset_at').first()

    def update_status(self, pk, status):
        obj = self.get(id=pk)
        obj.status = status
        obj.save()
        return obj

    def status_active(self, pk):
        return self.update_status(pk, NotificationStatus.ACTIVE)

    def status_failed(self, pk):
        return self.update_status(pk, NotificationStatus.FAILED)

    def status_success(self, pk):
        return self.update_status(pk, NotificationStatus.SUCCESS)

    def status_in_progress(self, pk):
        return self.update_status(pk, NotificationStatus.IN_PROGRESS)


class Notification(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_creator')
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, through='Participant',
        through_fields=('notification', 'user'), related_name='notification_participant'
    )
    title = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    onset_at = models.DateTimeField()
    status = models.IntegerField(choices=NotificationStatus.choices, default=NotificationStatus.ACTIVE)

    objects = NotificationManager()


class Participant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    status = models.IntegerField(choices=ParticipantStatus.choices, default=ParticipantStatus.ACTIVE)


@receiver(post_save, sender=Notification)
def on_update_notification(instance, created, **kwargs):
    from .storage import nearest_notification
    if created:
        if instance.status == NotificationStatus.ACTIVE:
            nearest_notification.check_and_update(instance.id, instance.onset_at)
    else:
        if instance.id == nearest_notification.pk:
            nearest_notification.update_from_db()
        else:
            if instance.status == NotificationStatus.ACTIVE:
                nearest_notification.check_and_update(instance.id, instance.onset_at)


@receiver(post_delete, sender=Notification)
def on_delete_notification(instance, **kwargs):
    from .storage import nearest_notification
    if instance.id == nearest_notification.pk:
        nearest_notification.update_from_db()
