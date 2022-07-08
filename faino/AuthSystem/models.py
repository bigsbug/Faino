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
    """Expire time fields and methods in abstract mode"""

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
    """Temp link for provide some files with security"""

    link = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True
    )
    ip = models.GenericIPAddressField()
    file = models.FileField()

    def is_valid_ip(self, ip: models.GenericIPAddressField) -> bool:
        return ip == self.ip


class UserConfirm(ExpireTime, models.Model):
    """confirm user activate wiht random code"""

    LENGTH_CODE: int = 5

    # Generate Random Code Between 0 to 9
    def generate_code() -> str:
        code = "".join(
            [str(random.randint(0, 9)) for _ in range(UserConfirm.LENGTH_CODE)]
        )
        return code

    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=LENGTH_CODE, default=generate_code, unique=True)
    token = models.UUIDField(default=uuid4, unique=True)

    def is_valid_code(self, input_code):
        return input_code == self.code

    def __str__(self) -> str:
        return self.code

    def save(self, *args, **kwargs):
        super(UserConfirm, self).save(*args, **kwargs)


class Endpoints(models.Model):
    """Creating a record for each endpoint for use in the permission system
    with the name of the endpoint and the class name and the app name"""

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


class PermissionGroup(models.Model):
    """Grouping a set of endpoints to create permissions
    for checking which users can use each endpoint"""

    name = models.CharField(max_length=20, unique=True)
    permissions = models.ManyToManyField(
        Endpoints,
        "endpoints",
    )

    def __str__(self):
        return self.name
