from django.urls import path
from .views import (
    Update_device,
)

app_name = "WEBSERVER"
urlpatterns = [
    # path("", index),
    path("update/<uuid:link>", Update_device, name="UPDATE_LINK"),
]
