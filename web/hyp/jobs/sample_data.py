from hyp.jobs.job_utils import retries
from hyp.data.generators import generate_sample_data

import django_rq, logging

logger = logging.getLogger(__name__)

def enqueue(experiment):
    logger.info(f'Enqueuing experiment sample data job for {experiment.id}')
    django_rq.enqueue(generate_sample_data, experiment, retry=retries())
