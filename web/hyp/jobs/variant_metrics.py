from datetime import datetime
from django.db import transaction
from hyp.models import DailyVariantMetrics, Variant
from hyp.jobs.job_utils import enqueue

import logging

logger = logging.getLogger(__name__)

def enqueue_all():
    date = datetime.now().date()
    jobs = []

    for variant in Variant.objects.all():
        job = enqueue(
            idempotency_key=f'{date}-metrics-for-variant-{variant.id}',
            func=create_variant_metrics,
            args=(variant, date)
        )

        if job is not None:
            jobs.append(job)

    return jobs

@transaction.atomic
def create_variant_metrics(variant, date):
    metric = DailyVariantMetrics(
        date=date,
        variant_id=variant.id,
        experiment_id=variant.experiment_id,
        conversion_rate=variant.conversion_rate(),
        traffic_split=variant.traffic_split_to_date(),
    )
    metric.save()
    logger.info(f'Variant metrics saved for {variant.id}')
