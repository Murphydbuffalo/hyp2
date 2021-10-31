from django.apps import AppConfig
from datetime import datetime


class HypConfig(AppConfig):
    name = 'hyp'

    def ready(self):
        from hyp import signals # noqa F401
        from hyp.jobs.variant_metrics import enqueue_all
        from hyp.models import IdempotencyKey

        import django_rq
        import logging

        logger = logging.getLogger(__name__)

        scheduler = django_rq.get_scheduler('default')

        logger.info('App starting up, calling HypConfig.ready()')

        idempotency_key = f'enqueue_variant_metrics_{datetime.now().date()}'

        if IdempotencyKey.objects.filter(key=idempotency_key).exists():
            return
        else:
            IdempotencyKey(key=idempotency_key).save()

            # Runs every day at 8:00AM UTC.
            # So for US time zones this will run at midnight/1:00AM/2:00AM/3:00AM or
            # 1:00AM/2:00AM/3:00AM/4:00AM depending on daylight savings time.
            # https://crontab.guru/every-day-at-2am
            scheduler.cron(
                "0 8 * * *",
                func=enqueue_all,
            )
