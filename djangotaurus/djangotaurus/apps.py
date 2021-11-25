from django.apps import AppConfig

class TaurusConfig(AppConfig):
    name = 'djangotaurus'

    def ready(self):
        from . import scheduler
        scheduler.start()