from email.policy import default
from rest_framework import serializers
from rest_framework import fields
from rest_framework.fields import UUIDField
from faino.WebServer.models import Device, Data, Type, Command, Button, UserDevice
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from rest_framework.fields import CurrentUserDefault


def CurrentUser(context):
    reqeust = context.get("request", None)
    if reqeust:
        return reqeust.user
    return None


class Serializer_UserDevice_INPUT_REQUEST(serializers.Serializer):
    name = serializers.CharField(max_length=24)
    type = serializers.ChoiceField(
        choices=["owner", "admin", "member"],
        # style={'base_template': 'radio.html'}
    )
    user = serializers.EmailField()


class Serializer_UserDevice(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = "__all__"


class Serializer_Profile(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = [
            "name",
            "type",
            "token",
            "join_time",
            "last_activate",
        ]


class Serializer_Buttons(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ["id", "control_name", "device", "is_star", "name", "array"]


class Serializer_Device(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=CurrentUserDefault())
    buttons = serializers.SerializerMethodField()
    user_profile = serializers.SerializerMethodField()

    @extend_schema_field(field=Serializer_Buttons(many=True))
    def get_buttons(self, *args, **kwargs):
        this_device = args[0]
        buttons_records = Button.objects.filter(device=this_device, is_star=True)[0:5]
        return Serializer_Buttons(buttons_records, many=True).data

    def get_user_profile(self, *args, **kwargs):

        user = CurrentUser(self.context)
        if user:
            this_device = args[0]
            userprofile = UserDevice.objects.get(device=this_device, user=user)
            return Serializer_Profile(userprofile).data
        raise ValueError('args not fund : "request"')

    class Meta:
        model = Device
        fields = [
            # "user",
            "name",
            "description",
            "token",
            "status",
            "type",
            "ip",
            "mac",
            "password",
            "buttons",
            "user_profile",
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
        fields = "__all__"
        # extra_kwargs = {"device": {"validators": []}}
