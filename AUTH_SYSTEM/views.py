from typing import Union
from typing_extensions import runtime
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import permissions, serializers
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
# from AUTH_SYSTEM.models import New_User
from AUTH_SYSTEM.serializer import Serializer_User
from django.contrib.auth.hashers import check_password, make_password


class User_API(APIView):
    permission_classes = []

    def hash_password(self, password: str) -> str:
        hashed_password: str = make_password(password)
        return hashed_password

    def post(self, requests) -> Union[Response, Http404]:
        data = requests.data
        serializer = Serializer_User(data=data)

        if serializer.is_valid(True):
            password: str = serializer.validated_data['password']
            hashed_password = self.hash_password(password)
            serializer.save(password=hashed_password)
            return Response(status=status.HTTP_201_CREATED)

    def get(self, reqeust) -> Union[Response]:
        serializer = Serializer_User(reqeust.user)
        return Response(serializer.data)

    def put(self, reqeust) -> Union[Response, Http404]:
        data = reqeust.data
        user = reqeust.user
        serializser = Serializer_User(user, data)
        if serializser.is_valid(True):
            serializser.save()
            return Response(status=status.HTTP_200_OK)
