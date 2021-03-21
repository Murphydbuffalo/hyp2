from django.apps import AppConfig


class HypConfig(AppConfig):
    name = 'hyp'

    def ready(self):
        from hyp import signals
