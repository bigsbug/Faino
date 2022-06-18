from functools import wraps
from typing import Union

from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import permissions, status
from rest_framework import response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status as Status

from faino.AuthSystem.models import New_User as USER
from faino.AuthSystem.models import Permissions_Group



from faino.WebServer.models import (
    Device as Device_Model,
    Command as Command_Model,
    Data as Data_Model,
    Button as Button_Model,
    UserDevice,
)

from .serializer import (
    Serializer_Device_Data,
    Serializer_Command,
    Serializer_Device,
    Serializer_Buttons,
    Serializer_Profile,
    Serializer_UserDevice,
    Serializer_UserDevice_INPUT_REQUEST,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from faino.AuthSystem.permissions import Auto_Detect_UserDevice

# Debug Options : set status of raise Errors in APIs
raise_exception_validitor = True


def decoretor_decrypt(func):
    @wraps(func)
    def inner(*args, **kwargs):
        # print(args)
        # print("-" * 20)
        # print(kwargs)
        return func(*args, **kwargs)

    return inner


class Device_API(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    ########################################################
    #                       Device                         #
    ########################################################
    def get_permissions(self):

        global_access = [
            "list",
            "create",
            "filter",
        ]

        if self.action in global_access:
            self.permission_classes = [
                permissions.IsAuthenticated,
            ]
        else:
            self.permission_classes = [
                permissions.IsAuthenticated,
                Auto_Detect_UserDevice,
            ]

        return [permission() for permission in self.permission_classes]

    @extend_schema(
        summary="Get All Devices of User",
        request={
            200: Serializer_Device,
        },
        responses={
            200: Serializer_Device(many=True),
            400: None,
        },
    )
    def list(self, request) -> Response:
        device = request.user.devices.all()
        serializer = Serializer_Device(device, many=True, context={"request": request})
        return Response(serializer.data, status=Status.HTTP_200_OK)

    @extend_schema(
        summary="Retrieve a special device with the UUID token ",
        responses={
            200: Serializer_Device,
            404: None,
        },
        parameters=[
            OpenApiParameter(
                name="id",
                description="Token of user",
                allow_blank=False,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, pk) -> Union[Response, Http404]:
        user = request.user
        device = get_object_or_404(user.UserDevice, token=pk).device
        serializer = Serializer_Device(device)
        return Response(serializer.data, status=Status.HTTP_200_OK)

    @extend_schema(
        summary="Full Update a Device",
        request=Serializer_Device,
        responses={
            200: Serializer_Device,
            404: None,
        },
        parameters=[
            OpenApiParameter(
                name="id",
                description="Token of user",
                allow_blank=False,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, pk) -> Response:
        user = request.user
        device = get_object_or_404(user.UserDevice, token=pk).device

        serializer = Serializer_Device(
            instance=device, data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Partial Update a Device",
        request=Serializer_Device,
        responses={
            200: Serializer_Device,
            404: None,
            400: Serializer_Device.default_error_messages,
        },
        parameters=[
            OpenApiParameter(
                name="id",
                description="Token of user",
                allow_blank=False,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, pk) -> Response:
        user = request.user
        device = get_object_or_404(user.UserDevice, token=pk).device

        serializer = Serializer_Device(
            instance=device,
            data=request.data,
            context={"request": request},
            partial=True,
        )

        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Create a new device",
        request=Serializer_Device,
        responses={201: Serializer_Device, 400: dict},
    )
    def create(self, request) -> Union[Response, Http404]:
        data = request.data

        serializer = Serializer_Device(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception_validitor):
            device = serializer.save()

            UserDevice(
                name="OWNER",
                user=request.user,
                device=device,
                type=Permissions_Group.objects.get(name="owner"),
            ).save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete Device with Token",
        responses={
            200: Serializer_Device,
            204: None,
        },
        parameters=[
            OpenApiParameter(
                name="id",
                description="Token of user",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, pk) -> Union[Response, None]:
        user = request.user
        device = get_object_or_404(user.UserDevice, token=pk).device
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Filter Device With Tyep  ",
        responses={
            200: Serializer_Device,
            404: None,
        },
        parameters=[
            OpenApiParameter(
                name="type",
                description="type of Device",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    @action(
        detail=False,
        methods=["GET"],
        url_path=r"filter/(?P<type>\w+)",
        url_name="filter_type",
    )
    def filter(self, request, type) -> Union[Response, Http404]:
        user = request.user
        device = get_list_or_404(user.devices, type=type)
        serializer = Serializer_Device(device, many=True)
        return Response(serializer.data, status=Status.HTTP_200_OK)

    ########################################################
    #                         Data                         #
    ########################################################

    @extend_schema(
        summary="get logs of the device",
        responses={
            200: Serializer_Device_Data,
            404: None,
        },
        parameters=[
            OpenApiParameter(
                name="id",
                description="Token of user",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    @action(detail=True, methods=["GET"], url_name="data")
    def data(self, request, pk) -> Union[Response, Http404]:
        user = request.user
        device = get_object_or_404(user.UserDevice, token=pk).device
        data_instance = get_list_or_404(Data_Model, device=device)
        serializer = Serializer_Device_Data(data_instance, many=True)

        return Response(serializer.data, status=Status.HTTP_200_OK)

    ########################################################
    #                       Command                        #
    ########################################################

    @extend_schema(
        summary="Get all commands",
        responses={
            200: Serializer_Command,
            404: OpenApiTypes.OBJECT,
        },
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description="Toekn Device",
            )
        ],
    )
    @action(detail=True, methods=["GET"], url_name="commands")
    # Retrieve Command
    def command(self, request, pk) -> Union[Response, Http404]:

        data = request.data
        device = get_object_or_404(request.user.UserDevice, token=pk).device
        status = get_list_or_404(Command_Model, device=device)
        serializer = Serializer_Command(status, many=True)
        return Response(serializer.data, status=Status.HTTP_200_OK)

    @extend_schema(
        summary="Send new command to the device",
        request=Serializer_Command,
        responses={
            200: Serializer_Command,
            404: OpenApiTypes.OBJECT,
        },
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description="Toekn Device",
            )
        ],
    )
    @command.mapping.post
    def create_command(self, request, pk) -> Response:
        data = request.data.copy()
        data["device"] = pk
        device = get_object_or_404(request.user.UserDevice, token=pk).device
        command_instace = None
        try:
            command_instace = Command_Model.objects.get(device=device)
        except:
            pass
        serializer = Serializer_Command(
            instance=command_instace, data=data, partial=True
        )
        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(data=serializer.data, status=Status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    ########################################################
    #                       Button                         #
    ########################################################

    @extend_schema(
        operation_id="button_RC",
        summary="Get all buttons of the Device",
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                description="Token Device",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: Serializer_Buttons,
            404: OpenApiTypes.OBJECT,
        },
    )
    @action(detail=True, url_name="buttons")
    def button(self, request, pk) -> Union[Response, Http404]:
        device = get_object_or_404(request.user.UserDevice, token=pk).device
        buttons = get_list_or_404(Button_Model, device=device)
        serializer = Serializer_Buttons(buttons, many=True)
        return Response(serializer.data, status=Status.HTTP_200_OK)

    @extend_schema(
        summary="Create new button",
        request=Serializer_Buttons,
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                description="Token Device",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: Serializer_Buttons,
            404: OpenApiTypes.OBJECT,
        },
    )
    @button.mapping.post
    def create_button(self, request, pk) -> Response:
        data = request.data.copy()
        data["device"] = pk
        serializer = Serializer_Buttons(data=data)
        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Retrieve a button",
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                description="Token Device",
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                "id_button",
                OpenApiTypes.NUMBER,
                description="ID of button",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: Serializer_Buttons,
            404: OpenApiTypes.OBJECT,
        },
    )
    @action(
        detail=True,
        url_path=r"buttons/(?P<id_button>\w+)",
        url_name="retrieve_button",
    )
    def retrieve_button(self, request, pk, id_button) -> Union[Response, Http404]:
        data = request.data
        device = get_object_or_404(request.user.UserDevice, token=pk).device
        button = get_object_or_404(Button_Model, device=device, pk=id_button)
        serializer = Serializer_Buttons(button)
        return Response(serializer.data, status=Status.HTTP_200_OK)

    @extend_schema(
        summary="Delete the button",
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                description="Token Device",
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                "id_button",
                OpenApiTypes.NUMBER,
                description="ID of button",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            204: OpenApiTypes.NONE,
            404: OpenApiTypes.OBJECT,
        },
    )
    @retrieve_button.mapping.delete
    def destroy_button(self, request, pk, id_button):
        device = get_object_or_404(request.user.UserDevice, token=pk).device
        button = get_object_or_404(Button_Model, device=device, pk=id_button)
        button.delete()
        return Response(status=Status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Full update the button",
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                description="Token Device",
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                "id_button",
                OpenApiTypes.NUMBER,
                description="ID of button",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: Serializer_Buttons,
            404: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
    )
    @retrieve_button.mapping.put
    def update_button(self, request, id_button, pk):
        data = request.data.copy()
        device = get_object_or_404(request.user.UserDevice, token=pk).device
        data["device"] = device.pk
        button = get_object_or_404(Button_Model, device=device, pk=id_button)
        serializer = Serializer_Buttons(button, data)
        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(serializer.data, status=Status.HTTP_200_OK)
        return Response(status=Status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Partial update the button",
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                description="Token Device",
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                "id_button",
                OpenApiTypes.NUMBER,
                description="ID of button",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: Serializer_Buttons,
            404: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
    )
    @retrieve_button.mapping.patch
    def update_partial_button(self, request, id_button, pk):
        device = get_object_or_404(request.user.UserDevice, token=pk).device
        button = get_object_or_404(Button_Model, device=device, pk=id_button)
        serializer = Serializer_Buttons(button, request.data, partial=True)
        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(serializer.data, status=Status.HTTP_200_OK)
        return Response(status=Status.HTTP_400_BAD_REQUEST)

    ########################################################
    #                       Users                          #
    ########################################################

    @extend_schema(
        summary="Get all users of device",
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                description="Token Device",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: Serializer_UserDevice,
            404: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
    )
    @action(
        detail=True,
        url_name="users",
    )
    def users(self, request, pk):
        user = request.user
        device = get_object_or_404(UserDevice, token=pk, user=request.user).device
        all_users = get_list_or_404(UserDevice, device=device)
        serializer = Serializer_Profile(all_users, many=True)
        return Response(serializer.data, status=Status.HTTP_200_OK)

    @extend_schema(
        summary="Create a user",
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                description="user token",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: Serializer_Profile,
            404: OpenApiTypes.OBJECT,
        },
        request=Serializer_UserDevice_INPUT_REQUEST,
    )
    @users.mapping.post
    def create_user(self, request, pk):
        data = request.data.copy()
        device = get_object_or_404(UserDevice, token=pk, user=request.user).device
        email = data.get("user", None)
        user = get_object_or_404(USER, email=email)
        data["device"] = device.token
        data["user"] = user.pk

        serializer = Serializer_UserDevice(data=data)
        if serializer.is_valid(True):
            try:
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            except:
                return Response(
                    data={"error": "this user added before to this device"},
                    status=Status.HTTP_406_NOT_ACCEPTABLE,
                )
        return Response(status=Status.HTTP_406_NOT_ACCEPTABLE)

    @extend_schema(
        summary="Retrieve a user",
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                description="user token",
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                "user_token",
                OpenApiTypes.UUID,
                description="target token",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: Serializer_Profile,
            404: OpenApiTypes.OBJECT,
        },
    )
    @action(
        detail=True,
        url_path=r"users/(?P<user_token>\w+)",
        url_name="retrieve user",
    )
    def retrieve_user(self, request, pk, user_token):
        user = user_token
        user_profile = get_object_or_404(UserDevice, token=user, user=request.user)
        serializer = Serializer_Profile(
            user_profile,
        )
        return Response(serializer.data, status=Status.HTTP_200_OK)

    @extend_schema(
        summary="Delete a user",
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                description="user token",
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                "user_token",
                OpenApiTypes.UUID,
                description="target token",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: Serializer_Profile,
            404: OpenApiTypes.OBJECT,
        },
    )
    @retrieve_user.mapping.delete
    def destory_user(self, request, pk, user_token):
        user = user_token
        user_profile = get_object_or_404(UserDevice, token=pk, user=request.user)
        user_profile.delete()
        return Response(status=Status.HTTP_200_OK)

    @extend_schema(
        summary="update a user",
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                description="user token",
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                "user_token",
                OpenApiTypes.UUID,
                description="target token",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: Serializer_Profile,
            404: OpenApiTypes.OBJECT,
        },
    )
    @retrieve_user.mapping.post
    def update_user(self, request, pk, user_token):
        user = user_token
        user_profile = get_object_or_404(UserDevice, token=pk, user=request.user)
        serializer = Serializer_Profile(user_profile, request.data)
        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(serializer.data, status=Status.HTTP_200_OK)
        return Response(status=Status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="update partial a user",
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.UUID,
                description="user token",
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                "user_token",
                OpenApiTypes.UUID,
                description="target token",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: Serializer_Profile,
            404: OpenApiTypes.OBJECT,
        },
    )
    @retrieve_user.mapping.patch
    def update_partial_user(self, request, pk, user_token):
        user = user_token
        user_profile = get_object_or_404(UserDevice, token=pk, user=request.user)
        serializer = Serializer_Profile(user_profile, request.data, partial=True)
        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(serializer.data, status=Status.HTTP_200_OK)
        return Response(status=Status.HTTP_400_BAD_REQUEST)
