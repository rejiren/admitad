import datetime
import json
import redis

from .models import Notification


client = redis.Redis(host='redis', port=6379)


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

    def get_data(self, key):
        return json.loads(client.get(self._redis_key)).get(key)

    def check_and_update(self, pk, onset_at):
        if self.onset_at > onset_at:
            self.update(pk, onset_at)

    @property
    def pk(self):
        return self.get_data(self._pk_key)

    @property
    def onset_at(self):
        return datetime.datetime.strptime(self.get_data(self._onset_at_key), '%Y-%m-%d %H:%M:%S%z')

    def update_from_db(self):
        n = self.get_nearest_from_db()
        self.update(n.id, n.onset_at)

    @staticmethod
    def get_nearest_from_db():
        return Notification.objects.nearest()

    def pop(self):
        notification = Notification.objects.status_in_progress(self.pk)
        self.update_from_db()
        return notification


nearest_notification = NearestNotification()
