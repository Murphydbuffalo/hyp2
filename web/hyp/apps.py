from django.apps import AppConfig


class HypConfig(AppConfig):
    name = 'hyp'

    def ready(self):
        from hyp import signals # noqa F401
        from hyp.jobs.variant_metrics import enqueue_all

        import django_rq, logging

        logger = logging.getLogger(__name__)

        scheduler = django_rq.get_scheduler('default')

        logger.info(f'App starting up, calling HypConfig.ready()')

        # Runs every day at 2:00AM Mountain / 8:00AM UTC
        # https://crontab.guru/every-day-at-2am
        scheduler.cron(
            "0 8 * * *",
            func=enqueue_all,
        )
