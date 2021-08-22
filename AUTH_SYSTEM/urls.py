from django.urls import path
from AUTH_SYSTEM.views import User_API

urlpatterns = [
    path('singin/', User_API.as_view(), name='USER_API'),
]
