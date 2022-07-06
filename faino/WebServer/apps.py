from django.apps import AppConfig


class WebServerppConfig(AppConfig):
    name = "faino.WebServer"

    def ready(self) -> None:
        from faino.WebServer import signals
