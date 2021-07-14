from rest_framework import  serializers
from rest_framework.fields import UUIDField
from .models import Device , Profile , Data , Type,NewStatus
from django.contrib.auth.models import User

class Serializer_Device(serializers.ModelSerializer):
    class Meta:
        model  = Device
        fields = '__all__'

class Serializer_Profile(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name','phone','company','membership']

class Serializer_User(serializers.ModelSerializer):
    profile = Serializer_Profile(Profile)
    class Meta:
        model = User
        fields = ['id','username','password','email','first_name','last_name','profile']

class Serializer_Device_Data(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['data','date']

class Serializer_Type (serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class Serializer_NewStatus(serializers.ModelSerializer):
    class Meta:
        model = NewStatus
        fields = ['data','complated','date']

class Serializer_Get_NewStatus(serializers.Serializer):
    data = serializers.JSONField()
    complated = serializers.BooleanField()
    token = serializers.UUIDField()