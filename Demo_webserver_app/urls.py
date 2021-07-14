from django.urls import path
# from .consumers import Device
from .views import index , Get_Device,Get_Info_User,Get_Data,Set_NewStatus
urlpatterns = [
    path('home/',index),
    path('devices/',Get_Device.as_view(),name='DEVICE'),
    path('info_user/',Get_Info_User.as_view(),name='INFO_USER'),
    path('data/',Get_Data.as_view(),name='GET_DATA'),
    path('status/',Set_NewStatus.as_view(),name='SET_NEWSTATUS'),
]