from datetime import datetime
from django.db import transaction
from hyp.models import DailyVariantMetrics, Variant
from hyp.jobs.job_utils import retries

import django_rq
import logging

logger = logging.getLogger(__name__)

# We've scheduled this to run every day at 8:00AM UTC via a CRON job
# So for US time zones this will run at midnight/1:00AM/2:00AM/3:00AM or
# 1:00AM/2:00AM/3:00AM/4:00AM depending on daylight savings time.
# https://crontab.guru/every-day-at-2am
# Can inspect the job via
# scheduler = django_rq.get_scheduler('default')
# jobs = list(scheduler.get_jobs())
def enqueue_all():
    for variant in Variant.objects.all():
        enqueue(variant)

def enqueue(variant):
    logger.info(f'Enqueuing variant metrics job for {variant.id}')
    django_rq.enqueue(create_variant_metrics, variant, retry=retries())

@transaction.atomic
def create_variant_metrics(variant):
    metric = DailyVariantMetrics(
        date=datetime.now().date(),
        variant_id=variant.id,
        experiment_id=variant.experiment_id,
        conversion_rate=variant.conversion_rate(),
        traffic_split=variant.traffic_split_to_date(),
    )
    metric.save()
    logger.info(f'Variant metrics saved for {variant.id}')
