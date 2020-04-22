from datetime import timedelta
from celery.task import periodic_task


@periodic_task(run_every=(timedelta(seconds=5)), name='hello')
def hello():
    print("Hello there")
