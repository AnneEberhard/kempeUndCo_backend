from django.apps import AppConfig


class FaminfosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'famInfos'

    def ready(self):
        from . import signals # noqa
