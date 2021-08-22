from django.db import models
from django.contrib.auth.models import AbstractUser


class New_User(AbstractUser):
    phone = models.CharField(max_length=11)
    company = models.fields.CharField(max_length=60, blank=True, null=True)
    membership = models.DateTimeField(blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
