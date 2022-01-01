from ast import walk
from time import time

from typing import Union
from django import http

from django.http import Http404
from django.http.response import HttpResponse

from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import permissions, status
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
from drf_spectacular.utils import extend_schema

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
    @extend_schema(
        description="get all devices of user ",
        request=HttpResponse,
        responses=[Serializer_Device],
        methods=["GET"],
    )
    def list(self, request) -> Response:
        device = get_list_or_404(Device_Model, user=request.user)
        serializer = Serializer_Device(device, many=True)
        return Response(serializer.data, status=Status.HTTP_200_OK)

    def retrieve(self, request, pk) -> Union[Response, Http404]:
        user = request.user
        device = get_object_or_404(Device_Model, token=pk, user=user)
        serializer = Serializer_Device(device)
        return Response(serializer.data, status=Status.HTTP_200_OK)

    def update(self, request, pk) -> Response:
        device = get_object_or_404(Device_Model, token=pk, user=request.user)

        serializer = Serializer_Device(
            instance=device, data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

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

    def create(self, request) -> Union[Response, Http404]:
        data = request.data

        serializer = Serializer_Device(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk) -> Union[Response, None]:

        device = get_object_or_404(Device_Model, token=pk, user=request.user)
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

    @action(detail=True, methods=["GET"], url_name="commands")
    def command(self, request, pk) -> Union[Response, Http404]:  # Retrieve Command

        data = request.data
        status = get_object_or_404(Command_Model, device=pk)
        serializer = Serializer_Command(status)
        return Response(serializer.data, status=Status.HTTP_200_OK)

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

    # @decoretor_decrypt
    @action(detail=True, url_name="buttons")
    def button(self, request, pk) -> Union[Response, Http404]:
        buttons = get_list_or_404(Button_Model, device=pk)
        serializer = Serializer_Buttons(buttons, many=True)
        return Response(serializer.data, status=Status.HTTP_200_OK)

    @button.mapping.post
    def button_create(self, request, pk) -> Response:
        data = request.data.copy()
        data["device"] = pk
        serializer = Serializer_Buttons(data=data)
        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        url_path=r"buttons/(?P<id>\w+)",
        # url_path=r"button_retrieve/(?P<id>[^/.]+)",
        # methods=["GET"],
        url_name="buttons_retrieve",
    )
    def button_retrieve(self, request, pk, id) -> Union[Response, Http404]:
        data = request.data
        device = pk
        button = get_object_or_404(Button_Model, device=device, pk=id)
        serializer = Serializer_Buttons(button)
        return Response(serializer.data, status=Status.HTTP_200_OK)

    @button_retrieve.mapping.delete
    def button_destroy(self, request, pk, id):
        device = pk
        button = get_object_or_404(Button_Model, device=device, pk=id)
        button.delete()
        return Response(status=Status.HTTP_204_NO_CONTENT)

    @button_retrieve.mapping.put
    def update_button(self, request, id, pk):
        data = request.data.copy()
        data["device"] = pk
        button = get_object_or_404(Button_Model, device=pk, pk=id)
        serializer = Serializer_Buttons(button, data)
        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(serializer.data, status=Status.HTTP_200_OK)
        return Response(status=Status.HTTP_400_BAD_REQUEST)

    @button_retrieve.mapping.patch
    def partial_update_button(self, request, id, pk):
        button = get_object_or_404(Button_Model, device=pk, pk=id)
        serializer = Serializer_Buttons(button, request.data, partial=True)
        if serializer.is_valid(raise_exception_validitor):
            serializer.save()
            return Response(serializer.data, status=Status.HTTP_200_OK)
        return Response(status=Status.HTTP_400_BAD_REQUEST)
