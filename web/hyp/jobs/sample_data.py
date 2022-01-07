from hyp.jobs import job_utils
from hyp.data.generators import generate_sample_data


def enqueue(experiment):
    job_utils.enqueue(idempotency_key=None, func=generate_sample_data, args=(experiment,))
