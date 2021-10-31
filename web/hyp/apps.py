from django.apps import AppConfig
from django.db.models.signals import post_migrate
from datetime import datetime

import django_rq
import logging


logger = logging.getLogger(__name__)


def enqueue_scheduled_jobs(sender, **kwargs):
    from hyp.jobs.variant_metrics import enqueue_all
    from hyp.models import IdempotencyKey

    scheduler = django_rq.get_scheduler('default')
    idempotency_key = f'enqueue_variant_metrics_{datetime.now().date()}'

    if IdempotencyKey.objects.filter(key=idempotency_key).exists():
        return
    else:
        IdempotencyKey(key=idempotency_key).save()

        # Runs every day at 8:00AM UTC.
        # So for US time zones this will run at midnight/1:00AM/2:00AM/3:00AM or
        # 1:00AM/2:00AM/3:00AM/4:00AM depending on daylight savings time.
        # https://crontab.guru/every-day-at-2am
        scheduler.cron("0 8 * * *", func=enqueue_all)


class HypConfig(AppConfig):
    name = 'hyp'

    def ready(self):
        logger.info('App starting up, calling HypConfig.ready()')

        from hyp import signals # noqa F401

        post_migrate.connect(enqueue_scheduled_jobs, sender=self)
