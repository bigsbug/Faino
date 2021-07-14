
from django.apps import AppConfig

class DemoWebserverAppConfig(AppConfig):
    name = 'Demo_webserver_app'

    def ready(self):
        pass
        from Demo_webserver_app import signals