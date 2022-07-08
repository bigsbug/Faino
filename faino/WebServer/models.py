from django.utils import timezone, tree
from django.db.models import constraints
from django.db import models
from django.core.exceptions import ValidationError

# from django.conf.global_settings import AUTH_USER_MODEL
from uuid import uuid4

from faino.AuthSystem.models import Permission

from django.conf import settings

User = settings.AUTH_USER_MODEL


def validator_name(name: str):
    unvlid_chars = [
        "-",
        "_",
        "(",
        ")",
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "+",
        "`",
        ":",
        ";",
        "/",
        "|",
        "\\",
        "<",
        ">",
        "?",
        "~",
        "[",
        "]",
        "{",
        "}",
        " ",
    ]

    def check_contin_char(char, val):
        return True in [True for item in char if item in val]

    if check_contin_char(unvlid_chars, name):

        raise ValidationError("The name Contain invalid character")


class Type(models.Model):
    name = models.CharField(
        max_length=62,
        primary_key=True,
        blank=False,
        unique=True,
        validators=[validator_name],
    )

    def __str__(self) -> str:
        return self.name


class Device(models.Model):
    token = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True
    )
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.fields.CharField(max_length=36)
    ip = models.CharField(max_length=64, blank=True)
    password = models.CharField(max_length=62, blank=True)
    mac = models.CharField(max_length=17, blank=True)
    description = models.fields.TextField(max_length=600, blank=True)
    users = models.ManyToManyField(User, "devices", through="UserDevice")

    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserDevice(models.Model):
    name = models.CharField(max_length=24)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="UserDevice"
    )
    device = models.ForeignKey(Device, models.CASCADE, related_name="UserDevice")
    type = models.ForeignKey(Permission, models.SET_NULL, null=True)

    token = models.UUIDField(default=uuid4, editable=False, unique=True)
    join_time = models.DateTimeField(auto_now_add=True)
    last_activate = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "device"], name="unique_field_userdevice"
            )
        ]

    def __str__(self):
        return f"{self.user}*{self.device}"


class Data(models.Model):
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="Data_Device"
    )
    data = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device.name


class Command(models.Model):
    choices_list = [
        ("CS", "Command Server"),
        ("CU", "Command User"),
    ]
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="Command_Device",
        # primary_key=True,
        # unique=True,
    )
    type = models.CharField(max_length=20, choices=choices_list)
    command = models.JSONField()
    status = models.fields.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    time_completed = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == True:
            self.time_completed = timezone.now()
        super().save(*args, *kwargs)

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


class Source_Device(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    version = models.FloatField(max_length=12)
    source = models.FileField(upload_to="sources")

    def __str__(self) -> str:
        return f"{self.type.name} : {self.version}"
