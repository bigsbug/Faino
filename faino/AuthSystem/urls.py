from os import name
from re import I
from django.db.models.fields.related import ForeignKey
from django.urls import path
from faino.AuthSystem.views import (
    Forget_Password,
    User_API,
    Confrim_Email,
)
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register("user", User, basename="USER_API")
# urlpatterns = router.urls

urlpatterns = [
    path("auth/singup/", User_API.as_view(), name="USER_API"),
    path("auth/forget_password/", Forget_Password.as_view(), name="FORGET_PASSWROD"),
    path("auth/confirm_email/", Confrim_Email.as_view(), name="CONFIRM_EMAIL"),
]
