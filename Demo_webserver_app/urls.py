from django.urls import path
# from .consumers import Device
from .views import index , Get_Device,Get_Info_User
urlpatterns = [
    path('home/',index),
    path('devices/',Get_Device.as_view(),name='DEVICE'),
    path('info_user/',Get_Info_User.as_view(),name='INFO_USER'),
]