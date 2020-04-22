from datetime import timedelta
import time
from celery.task import periodic_task, PeriodicTask
from celery import shared_task
from celery import group, chord


@shared_task
def send_mail(email='asdasdasd'):
    time.sleep(4)
    print(email)
    time.sleep(4)
    return 1, email


@shared_task
def send_mail_callback(result):
    print(result)
    return result


@shared_task
def send_event_callback(result):
    print('event callback')
    print(result)
    return result


@periodic_task(run_every=(timedelta(seconds=5)), name='hello')
def hello():
    print("Start")
    job = group([
        send_mail.s('email1') | send_mail_callback.s(),
        send_mail.s('email2') | send_mail_callback.s()
    ]) | send_event_callback.s()
    job.apply_async()
    print("End")
