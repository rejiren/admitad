import datetime
import json
import redis
from django.conf import settings
from .models import Notification


client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class NearestNotification:
    _redis_key = 'nearest_notification'
    _pk_key = 'id'
    _onset_at_key = 'onset_at'

    def __init__(self):
        self.update_from_db()

    def update(self, pk, onset_at):
        client.set(self._redis_key, json.dumps({
            self._pk_key: pk,
            self._onset_at_key: str(onset_at)
        }))

    def init_redis_data(self):
        client.set(self._redis_key, json.dumps({}))

    def get_data(self, key):
        return json.loads(client.get(self._redis_key)).get(key)

    def check_and_update(self, pk, onset_at):
        if self.pk is None or self.onset_at > onset_at:
            self.update(pk, onset_at)

    @property
    def pk(self):
        return self.get_data(self._pk_key)

    @property
    def onset_at(self):
        if self.pk:
            return datetime.datetime.strptime(self.get_data(self._onset_at_key), '%Y-%m-%d %H:%M:%S%z')

    def update_from_db(self):
        notification = self.get_nearest_from_db()
        if notification:
            self.update(notification.id, notification.onset_at)
        else:
            self.init_redis_data()

    @staticmethod
    def get_nearest_from_db():
        return Notification.objects.nearest()

    def pop(self):
        notification = Notification.objects.status_in_progress(self.pk)
        self.update_from_db()
        return notification


nearest_notification = NearestNotification()
