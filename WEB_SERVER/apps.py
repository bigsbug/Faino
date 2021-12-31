from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    name = "WEB_SERVER"

    def ready(self):
        from WEB_SERVER import signals
