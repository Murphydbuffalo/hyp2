from hyp.models import IdempotencyKey
from rq import Retry

import django_rq


def retries(max=5, interval=[4, 16, 64, 256, 1028]):
     return Retry(max=max, interval=interval)

def clear_scheduled_jobs():
     for job in get_scheduled_jobs():
          job.delete()

def get_scheduled_jobs():
     return get_scheduler().get_jobs()

def get_scheduler():
     return django_rq.get_scheduler()
