from rest_framework import serializers
from rest_framework import fields
from rest_framework.fields import UUIDField
from WEB_SERVER.models import Device, Data, Type, Command, Button
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class Serializer_Buttons(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ["id", "control_name", "device", "is_star", "name", "array"]


class Serializer_Device(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    buttons = serializers.SerializerMethodField()

    @extend_schema_field(field=Serializer_Buttons(many=True))
    def get_buttons(self, *args, **kwargs):
        this_device = args[0]
        buttons_records = Button.objects.filter(device=this_device, is_star=True)[0:5]
        return Serializer_Buttons(buttons_records, many=True).data

    class Meta:
        model = Device
        fields = [
            "user",
            "name",
            "description",
            "token",
            "status",
            "type",
            "ip",
            "mac",
            "password",
            "buttons",
        ]


class Serializer_Device_Data(serializers.ModelSerializer):
    read_only = True

    class Meta:
        model = Data
        fields = ["data", "date"]


class Serializer_Type(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class Serializer_Command(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ["data", "status", "date", "device"]
        # extra_kwargs = {"device": {"validators": []}}
