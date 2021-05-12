from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,editable=False,primary_key=True)
    name = models.fields.CharField(max_length=36,blank=False)
    company = models.fields.CharField(max_length=60,blank=True)
     
    def __str__(self):
        return self.name
    

class Device(models.Model):
    status = [
        (True,'ON'),
        (False,'OFF')
    ]
    token = models.UUIDField(primary_key=True,default=uuid4,editable=False,unique=True)
    name = models.fields.CharField(max_length=36)
    description = models.fields.TextField(max_length=600,blank=True)
    users = models.ForeignKey(Profile,related_name='Device_user',on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Data(models.Model):
    device = models.ForeignKey(Device,on_delete=models.CASCADE,related_name='Data_Device')
    data = models.JSONField()

    def __str__(self):
        return self.device.name

class NewStatus(models.Model):
    device = models.OneToOneField(Device,on_delete=models.CASCADE,related_name="New_Status_Device",primary_key=True,unique=True)
    data = models.JSONField()
    complated = models.fields.BooleanField(default=False)

    def __str__(self):
        return self.device.name