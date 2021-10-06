from django.db import router
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import Device

Router = DefaultRouter()
app_name = 'api'
Router.register("device", Device, basename="Device")
urlpatterns = Router.urls
