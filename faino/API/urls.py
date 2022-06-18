from django.db import router
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import Device_API
from faino.AuthSystem.urls import urlpatterns as auth_urls

Router = DefaultRouter()
app_name = "api"
Router.register("device", Device_API, basename="Device")
urlpatterns = Router.urls + auth_urls
