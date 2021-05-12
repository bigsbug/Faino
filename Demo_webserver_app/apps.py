
from django.apps import AppConfig

class DemoWebserverAppConfig(AppConfig):
    name = 'Demo_webserver_app'

    def ready(self):
        from Demo_webserver_app import signals