from django.urls import path
# from .consumers import Device
from .views import index
urlpatterns = [
    path('home/',index),
]