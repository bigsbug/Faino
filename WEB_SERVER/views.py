from collections import namedtuple

from time import time

from typing import Union

from django.http import HttpResponse, Http404

from django.shortcuts import get_object_or_404, get_list_or_404

from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt

from rest_framework import permissions, status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status as Status

from .models import Device, Type, Command, Data, Button

from .serializer import (
    Serializer_Device_Data,
    Serializer_Command,
    Serializer_Device,
    Serializer_Buttons,
)


def index(request) -> HttpResponse:
    return HttpResponse("Your Connected to WebServer")


class Get_Device(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        device = get_list_or_404(Device, user=request.user)
        data = Serializer_Device(device, many=True).data
        return Response(data)

    def post(self, request) -> Union[Response, Http404]:

        self.data = request.data
        self.user = request.user
        serializers = self.Filter_Device()

        return Response(serializers.data)

    def Filter_Device(self) -> Union[Http404, Serializer_Device]:

        if "token" in self.data:
            try:

                data = get_object_or_404(Device,
                                         token=self.data["token"],
                                         user=self.user)

                return Serializer_Device(data)

            except:
                raise Http404("token is not valid")

        else:

            if "type" in self.data:

                try:

                    NameType = get_object_or_404(Type, name=self.data["type"])
                    device = get_list_or_404(
                        Device, type=NameType, user=self.user)
                    return Serializer_Device(device, many=True)

                except:
                    raise Http404()

            else:
                raise Http404()


class CUD_Device(APIView):  # Create Update Delete Device
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request) -> Response:
        if "token" in request.data:
            token = request.data["token"]
            try:
                device = get_object_or_404(Device,
                                           token=token,
                                           user=request.user)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            serializer = Serializer_Device(instance=device,
                                           data=request.data,
                                           context={"request": request})

            if serializer.is_valid(True):

                serializer.save()

                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request) -> Union[Response, ]:

        if "token" in request.data:
            token = request.data["token"]
            try:
                device = get_object_or_404(Device,
                                           token=token,
                                           user=request.user)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            device.delete()

            return Response(status=status.HTTP_202_ACCEPTED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request) -> Union[Response, Http404]:
        data = request.data

        serializer = Serializer_Device(data=request.data,
                                       context={"request": request})
        if serializer.is_valid(True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)


class Get_Data(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request) -> Union[Response, Http404]:

        user = request.user
        token = request.data["token"]

        device = get_object_or_404(Device, user=user, token=token)

        print(device)

        data_instance = get_list_or_404(Data, device=device)
        serializer = Serializer_Device_Data(data_instance, many=True)

        return Response(serializer.data)


class Get_Command(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request) -> Union[Response, Http404]:

        data = request.data

        if ("token" not in data
            ):  # check token exist in reqeust if not reject the request user
            return Response(data="HTTP 400 BAD REQUEST",
                            status=Status.HTTP_400_BAD_REQUEST)

        token = data["token"]

        device = get_object_or_404(Device, user=request.user, token=token)
        status = get_object_or_404(Command, device=device)

        serializer = Serializer_Command(status)
        return Response(serializer.data)


class New_Command(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request) -> Response:
        data = request.data
        serializer = Serializer_Command(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data="HTTP 201 CREATED",
                            status=Status.HTTP_201_CREATED)
        else:
            return Response(data="HTTP 400 BAD REQUEST",
                            status=Status.HTTP_400_BAD_REQUEST)


class New_Button(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request) -> Response:
        data = request.data

        serializer = Serializer_Buttons(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)


class Get_Buttons(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request) -> Union[Response, Http404]:
        data = request.data
        if ("device" not in data
            ):  # check device exist in reqeust if not reject the request user
            return Response(status=status.HTTP_400_BAD_REQUEST)

        device_token = data["device"]

        buttons = get_list_or_404(Button, device=device_token)
        serializer = Serializer_Buttons(buttons, many=True)
        return Response(serializer.data, status=Status.HTTP_200_OK)
