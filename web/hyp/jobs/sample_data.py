from hyp.jobs.job_utils import enqueue
from hyp.data.generators import generate_sample_data


def enqueue(experiment):
    enqueue(func=lambda: generate_sample_data(experiment))
