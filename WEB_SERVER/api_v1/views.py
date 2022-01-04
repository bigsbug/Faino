from ast import Str, walk
from time import time

from typing import Union
from django import http

from django.http import Http404
from django.http.response import HttpResponse

from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import permissions, status
from rest_framework import response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status as Status
from functools import partial, wraps

from WEB_SERVER.models import (
    Device as Device_Model,
    Command as Command_Model,
    Data as Data_Model,
    Button as Button_Model,
)

from .serializer import (
    Serializer_Device_Data,
    Serializer_Command,
    Serializer_Device,
    Serializer_Buttons,
)
<<<<<<< HEAD
from drf_spectacular.utils import extend_schema
=======
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
>>>>>>> feature/swagger-openapi3

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


class Device(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    ########################################################
    #                       Device                         #
    ########################################################
<<<<<<< HEAD
=======

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
>>>>>>> feature/swagger-openapi3
    def list(self, request) -> Response:
        device = get_list_or_404(Device_Model, user=request.user)
        serializer = Serializer_Device(device, many=True)
        return Response(serializer.data, status=Status.HTTP_200_OK)

    @extend_schema(
        summary="Retrive a special device with the UUID token",
        responses={
            200: Serializer_Device,
            404: None,
        },
        parameters=[
            OpenApiParameter(
                name="id",
                description="Token of Device",
                allow_blank=False,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, pk) -> Union[Response, Http404]:
        user = request.user
        device = get_object_or_404(Device_Model, token=pk, user=user)
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
                description="Token of Device",
                allow_blank=False,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, pk) -> Response:
        device = get_object_or_404(Device_Model, token=pk, user=request.user)

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
                description="Token of Device",
                allow_blank=False,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, pk) -> Response:
        device = get_object_or_404(Device_Model, token=pk, user=request.user)

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
            serializer.save()
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
                description="Token of Device",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, pk) -> Union[Response, None]:

        device = get_object_or_404(Device_Model, token=pk, user=request.user)
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
        device = get_list_or_404(Device_Model, type=type, user=user)
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
                description="Token of Device",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    @action(detail=True, methods=["GET"], url_name="data")
    def data(self, request, pk) -> Union[Response, Http404]:
        user = request.user
        token = pk
        device = get_object_or_404(Device_Model, user=user, token=token)
        data_instance = get_list_or_404(Data_Model, device=device)
        serializer = Serializer_Device_Data(data_instance, many=True)

        return Response(serializer.data, status=Status.HTTP_200_OK)

    ########################################################
    #                       Command                        #
    ########################################################

<<<<<<< HEAD
    @action(detail=True, methods=["GET"], url_name="commands")
=======
    @extend_schema(
        summary="Get the last command",
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
    @action(detail=True, methods=["GET"], url_name="command")
>>>>>>> feature/swagger-openapi3
    def command(self, request, pk) -> Union[Response, Http404]:  # Retrieve Command

        data = request.data
        status = get_object_or_404(Command_Model, device=pk)
        serializer = Serializer_Command(status)
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
    def command_create(self, request, pk) -> Response:
        data = request.data.copy()
        data["device"] = pk
        command_instace = None
        try:
            command_instace = Command_Model.objects.get(device=pk)
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

<<<<<<< HEAD
    # @decoretor_decrypt
    @action(detail=True, url_name="buttons")
=======
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
    @action(detail=True, url_name="button")
>>>>>>> feature/swagger-openapi3
    def button(self, request, pk) -> Union[Response, Http404]:
        buttons = get_list_or_404(Button_Model, device=pk)
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
    def button_create(self, request, pk) -> Response:
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
<<<<<<< HEAD
        url_path=r"buttons/(?P<id>\w+)",
        # url_path=r"button_retrieve/(?P<id>[^/.]+)",
        # methods=["GET"],
        url_name="buttons_retrieve",
=======
        url_path=r"button/(?P<id_button>\w+)",
        url_name="button_retrieve",
>>>>>>> feature/swagger-openapi3
    )
    def button_retrieve(self, request, pk, id_button) -> Union[Response, Http404]:
        data = request.data
        device = pk
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
    @button_retrieve.mapping.delete
    def button_destroy(self, request, pk, id_button):
        device = pk
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
    @button_retrieve.mapping.put
    def update_button(self, request, id_button, pk):
        data = request.data.copy()
        data["device"] = pk
        button = get_object_or_404(Button_Model, device=pk, pk=id_button)
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
    @button_retrieve.mapping.patch
    def partial_update_button(self, request, id_button, pk):
        button = get_object_or_404(Button_Model, device=pk, pk=id_button)
        serializer = Serializer_Buttons(button, request.data, partial=True)
        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(serializer.data, status=Status.HTTP_200_OK)
        return Response(status=Status.HTTP_400_BAD_REQUEST)
