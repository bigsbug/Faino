from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("", consumers.Device_WB.as_asgi()),
]
