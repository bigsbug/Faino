from rest_framework import fields, serializers

from django.conf import settings
from AUTH_SYSTEM.models import New_User, Confirm_User


class Serializer_User(serializers.ModelSerializer):
    class Meta:
        model = New_User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'phone',
            'company',
            'membership',
        ]


class Serializer_Confirm_User(serializers.ModelSerializer):
    class Meta:
        model = Confirm_User
        fields = '__all__'