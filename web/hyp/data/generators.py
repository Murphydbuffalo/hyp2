from django.db import transaction
from hyp.models import DailyVariantMetrics, Interaction
from hyp.thompson_sampler import ThompsonSampler
from datetime import datetime, timedelta

import logging, random

logger = logging.getLogger(__name__)

def generate_random_conversion_rates(experiment, lower_bound=0.02, upper_bound=0.10):
    conversion_rates = {}

    for variant in experiment.variant_set.all():
        conversion_rates[variant.id] = random.uniform(lower_bound, upper_bound)

    return conversion_rates


@transaction.atomic
def generate_sample_data(experiment, conversion_rates=None, days_to_backfill=90, interactions_per_day=30):
    original_metrics_count = DailyVariantMetrics.objects.filter(experiment=experiment).count()
    original_interaction_count = Interaction.objects.filter(experiment=experiment).count()

    if conversion_rates is None:
        conversion_rates = generate_random_conversion_rates(experiment)

    variants = experiment.variant_set.all()
    for lookback_days in range(days_to_backfill, 0, -1):
        lookback_date = datetime.now().date() - timedelta(days=lookback_days)
        created_at = datetime(year=lookback_date.year, month=lookback_date.month, day=lookback_date.day)

        for _i in range(interactions_per_day):
            variant = ThompsonSampler(variants).winner()
            interaction = Interaction(
                variant=variant,
                experiment=experiment,
                customer=experiment.customer,
                participant_id=f'Participant {random.random()}',
                created_at=created_at,
            )
            interaction.save()

            # Set `converted` in separate query so that database trigger
            # updates counter cache fields on Variant
            if random.random() <= conversion_rates[variant.id]:
                interaction.converted = True
                interaction.save()

            variant.refresh_from_db()

        for variant in variants:
            metric = DailyVariantMetrics(
                date=lookback_date,
                variant_id=variant.id,
                experiment_id=experiment.id,
                conversion_rate=variant.conversion_rate(),
                traffic_split=variant.traffic_split_to_date(),
            )
            metric.save()

    new_interaction_count = Interaction.objects.filter(experiment=experiment).count()
    new_metrics_count = DailyVariantMetrics.objects.filter(experiment=experiment).count()

    logger.info(f'Created {new_interaction_count - original_interaction_count} random interactions for {experiment.name}')
    logger.info(f'Created {new_metrics_count - original_metrics_count} daily metrics for {experiment.name}')
