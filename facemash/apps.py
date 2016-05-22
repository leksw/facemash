from django.apps import AppConfig


class FacemashConfig(AppConfig):
    name = 'facemash'

    def ready(self):
        import facemash.signals  # noqa
