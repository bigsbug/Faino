from django.urls import path
from django.conf.urls import include
from .views import (
    index,
    # Get_Device,
    # New_Command,
    # Get_Command,
    # New_Button,
    # Get_Buttons,
    # Get_Data,
    # CUD_Device,
    Update_device,
)

app_name = "WEBSERVER"
urlpatterns = [
    # path("", index),
    path("update/<uuid:link>", Update_device, name="UPDATE_LINK"),
]
