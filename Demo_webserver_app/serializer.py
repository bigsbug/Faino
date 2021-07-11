from rest_framework import  serializers
from .models import Device , Profile , Data
from django.contrib.auth.models import User

class serializer_Device(serializers.ModelSerializer):
    class Meta:
        model  = Device
        fields = '__all__'

class serializer_Profile(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name','phone','company','membership']

class Serializer_User(serializers.ModelSerializer):
    profile = serializer_Profile(Profile)
    class Meta:
        model = User
        fields = ['id','username','password','email','first_name','last_name','profile']

class Serializer_Device_Data(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'