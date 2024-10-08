from django.apps import AppConfig


class AncestorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ancestors'

    def ready(self):
        from . import signals # noqa
