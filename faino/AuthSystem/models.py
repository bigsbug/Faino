import random
from datetime import timedelta
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


def create_expire_time(days=0, seconds=0, minutes=0, hours=0, weeks=0):

    return timezone.now() + timedelta(
        days=days,
        seconds=seconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks,
    )


class ExpireTime(models.Model):
    def expire_time():
        return create_expire_time(seconds=10)

    expire = models.DateTimeField(default=expire_time)

    def is_expired(self) -> bool:
        return self.expire > timezone.now()

    class Meta:
        abstract = True


class NewUser(AbstractUser):
    phone = models.CharField(max_length=11, unique=True)
    company = models.fields.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(unique=True)
    membership = models.DateTimeField(blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)


class TempLink(ExpireTime, models.Model):

    link = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True
    )
    ip = models.GenericIPAddressField()
    file = models.FileField()

    def check_ip(self, ip: models.GenericIPAddressField) -> bool:
        return ip == self.ip


class UserConfirm(ExpireTime, models.Model):
    LENGTH_CODE: int = 5

    # Generate Random Code Between 0 to 9
    def generate_code(length: int = 5) -> str:
        code = "".join([str(random.randint(0, 9)) for _ in range(LENGTH_CODE)])
        return code

    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=LENGTH_CODE, default=generate_code, unique=True)
    token = models.UUIDField(default=uuid4, unique=True)

    def valid_code(self, input_code):
        return input_code == self.code

    def __str__(self) -> str:
        return self.code

    def save(self, *args, **kwargs):
        print(args, kwargs)
        super(UserConfirm, self).save(*args, **kwargs)


class Permissions(models.Model):
    name = models.CharField(max_length=100)
    app_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "app_name", "class_name"], name="unique_id"
            )
        ]

    def __str__(self):
        return f"{self.app_name} | {self.class_name} | {self.name}"


class Permissions_Group(models.Model):
    name = models.CharField(max_length=20, unique=True)
    permissions = models.ManyToManyField(
        Permissions,
        "Permissions_of_group",
    )

    def __str__(self):
        return self.name
