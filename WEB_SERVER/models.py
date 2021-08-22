from django.utils import timezone, tree
from django.db.models import constraints
from django.db import models
# from django.conf.global_settings import AUTH_USER_MODEL
from uuid import uuid4

from django.conf import settings

User = settings.AUTH_USER_MODEL


class Type(models.Model):
    name = models.CharField(max_length=62,
                            primary_key=True,
                            blank=False,
                            unique=True)

    def __str__(self) -> str:
        return self.name


class Device(models.Model):
    token = models.UUIDField(primary_key=True,
                             default=uuid4,
                             editable=False,
                             unique=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.fields.CharField(max_length=36)
    ip = models.GenericIPAddressField(blank=True, null=True)
    password = models.CharField(max_length=62, blank=True)
    mac = models.CharField(max_length=17, blank=True)
    description = models.fields.TextField(max_length=600, blank=True)
    user = models.ForeignKey(User,
                             related_name="Device_user",
                             on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Data(models.Model):
    device = models.ForeignKey(Device,
                               on_delete=models.CASCADE,
                               related_name="Data_Device")
    data = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device.name


class Command(models.Model):
    device = models.OneToOneField(
        Device,
        on_delete=models.CASCADE,
        related_name="Command_Device",
        primary_key=True,
        unique=True,
    )
    data = models.JSONField()
    complated = models.fields.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device.name


class Button(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    control_name = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    array = models.TextField()
    is_star = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.control_name
