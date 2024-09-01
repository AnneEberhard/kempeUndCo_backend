from django.apps import AppConfig


class InfosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'infos'

    def ready(self):
        from . import signals # noqa
