from hyp.models import IdempotencyKey
from rq import Retry

import django_rq
import logging

logger = logging.getLogger(__name__)


# Force callers to specify if they don't want a job to be idempotent
def enqueue(idempotency_key, func):
     logger.info(f'Enqueuing job for function {func.__name__} with idempotency key {idempotency_key}')

     return IdempotencyKey.call_once(
          func=lambda: django_rq.enqueue(func, retry=retries()),
          key=idempotency_key,
     )

def retries(max=5, interval=[4, 16, 64, 256, 1028]):
     return Retry(max=max, interval=interval)

def clear_scheduled_jobs():
     for job in get_scheduled_jobs():
          job.delete()

def get_scheduled_jobs():
     return get_scheduler().get_jobs()

def get_scheduler():
     return django_rq.get_scheduler()
