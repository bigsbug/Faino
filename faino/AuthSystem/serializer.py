from rest_framework import fields, serializers

from django.conf import settings
from faino.AuthSystem.models import NewUser, UserConfirm


class Serializer_User(serializers.ModelSerializer):
    class Meta:
        model = NewUser
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
        model = UserConfirm
        fields = "__all__"


class Serializer_Confirm(serializers.Serializer):
    code = serializers.CharField(max_length=8)
    email = serializers.EmailField()


class Serializer_Confirm_Forget(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=UserConfirm.LENGTH_CODE)
    password = serializers.CharField(max_length=60)
    password2 = serializers.CharField(max_length=60)
