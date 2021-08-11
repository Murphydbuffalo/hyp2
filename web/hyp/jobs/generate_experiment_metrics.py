from datetime import datetime
from django.db import transaction
from hyp.models import DailyVariantMetrics, Experiment
from hyp.jobs.job_utils import retries

import django_rq


def enqueue(experiment_id):
    experiment = Experiment.objects.get(pk=experiment_id)

    django_rq.enqueue(create_variant_metrics, experiment, retry=retries())

@transaction.atomic
def create_variant_metrics(experiment):
    for variant in experiment.variant_set.all():
        metric = DailyVariantMetrics(
            date=datetime.now().date(),
            variant_id=variant.id,
            experiment_id=experiment.id,
            conversion_rate=variant.conversion_rate(),
            traffic_split=variant.traffic_split_to_date(),
        )
        metric.save()
