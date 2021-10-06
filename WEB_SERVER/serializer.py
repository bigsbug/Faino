from rest_framework import serializers
from rest_framework import fields
from rest_framework.fields import UUIDField
from WEB_SERVER.models import Device, Data, Type, Command, Button
from django.contrib.auth.models import User


class Serializer_Buttons(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ["id", "control_name", "device", "is_star", "name", "array"]


class Serializer_Device(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    buttons = serializers.SerializerMethodField()

    def get_buttons(self, *args, **kwargs):
        this_device = args[0]
        return Serializer_Buttons(
            Button.objects.filter(device=this_device)[0:5], many=True).data

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
        fields = ["data", "complated", "date", "device"]
        extra_kwargs = {"device": {"validators": []}}
