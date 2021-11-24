from hyp.jobs.job_utils import clear_scheduled_jobs, get_scheduled_jobs, get_scheduler
from hyp.jobs.variant_metrics import enqueue_all
from django_rq.management.commands import rqscheduler

import logging

scheduler = get_scheduler()
logger = logging.getLogger(__name__)


def register_scheduled_jobs():
    # Every day at 8:00AM UTC: https://crontab.guru/every-day-at-2am
    # So for US time zones this will run at midnight/1:00AM/2:00AM/3:00AM or
    # 1:00AM/2:00AM/3:00AM/4:00AM depending on daylight savings time.
    scheduler.cron("0 8 * * *", func=enqueue_all)

    logger.info("The following jobs have been scheduled:") 

    for job in get_scheduled_jobs():
        logger.info(f'Function {job.func.__name__}')


class Command(rqscheduler.Command):
    def handle(self, *args, **kwargs):
        # Sadly, RQ scheduler duplicates enqueued jobs every time the
        # app restarts: https://github.com/rq/rq-scheduler/issues/51
        # So, we clear out any existing scheduled jobs and re-schedule
        # here.
        clear_scheduled_jobs()
        register_scheduled_jobs()
        super(Command, self).handle(*args, **kwargs)