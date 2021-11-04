from django.apps import AppConfig
from django.db.models.signals import post_migrate
from datetime import datetime

import django_rq
import logging


logger = logging.getLogger(__name__)


# Able to import models in this function
def postMigrate(sender, **kwargs):
    logger.info('Running postMigrate()')
    pass


class HypConfig(AppConfig):
    name = 'hyp'

    def ready(self):
        logger.info('App starting up, calling HypConfig.ready()')

        from hyp import signals # noqa F401

        post_migrate.connect(postMigrate, sender=self)
