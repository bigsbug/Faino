from rest_framework import fields, serializers

from django.conf import settings
from faino.AuthSystem.models import New_User, Confirm_User


class Serializer_User(serializers.ModelSerializer):
    class Meta:
        model = New_User
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "phone",
            "company",
            "membership",
        ]


class Serializer_Confirm_User(serializers.ModelSerializer):
    class Meta:
        model = Confirm_User
        fields = "__all__"


class Serializer_Confirm(serializers.Serializer):
    code = serializers.CharField(max_length=8)
    email = serializers.EmailField()


class Serializer_Confirm_Forget(serializers.Serializer):
    code = serializers.CharField(max_length=8)
    password = serializers.CharField(max_length=60)
    password2 = serializers.CharField(max_length=60)
