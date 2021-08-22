"""
ASGI config for WebServer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from WEB_SERVER.authMiddlware import MiddleWareStack_authToken
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from WEB_SERVER.router import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebServer.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": MiddleWareStack_authToken(URLRouter(websocket_urlpatterns)),
    }
)
