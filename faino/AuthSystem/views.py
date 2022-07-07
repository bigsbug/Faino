from typing import Union

from django.http.response import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework import permissions
from rest_framework import permissions
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.reverse import django_reverse

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from faino.AuthSystem.serializer import (
    Serializer_Confirm_Forget,
    Serializer_User,
    Serializer_Confirm_User,
    Serializer_Confirm,
)
from faino.AuthSystem.models import NewUser, Confirm_User


def SendEmail(subject: str, body: str, email: list, html: str):
    email = EmailMultiAlternatives(
        subject,
        body,
        to=email,
    )
    email.attach_alternative(html, "text/html")

    email.send()


class Confrim_Email(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Sended activation code to email",
        parameters=[
            OpenApiParameter(
                name="email",
                type=OpenApiTypes.EMAIL,
                allow_blank=False,
            )
        ],
    )
    def get(self, request):

        data = request.data.copy()
        data["expire"] = Confirm_User.expire_time()
        data["code"] = Confirm_User.random_code()

        email_address = request.GET.get("email", None)
        confrim_model = None
        try:
            user = NewUser.objects.get(email=email_address)
            data["user"] = user.pk
        except:
            return HttpResponse("invalid user")
        if user.is_active == True:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            confrim_model = Confirm_User.objects.get(user=user)
        except:
            pass

        confirm = Serializer_Confirm_User(
            instance=confrim_model, data=data, partial=True
        )
        if confirm.is_valid(True):
            confirm = confirm.save()
        template = "verify_account.html"
        context = {
            "active_code": confirm.code,
            "domain": request.META["HTTP_HOST"],
        }
        html_template = render_to_string(template, context)

        SendEmail(
            "کد احراز هویت",
            "کد احراز هویت شما {confirm.code} میباشد",
            [user.email],
            html_template,
        )

        return HttpResponse("check your email")

    @extend_schema(
        summary="Confirm activation code ",
        request={"application/x-www-form-urlencoded": Serializer_Confirm},
    )
    def post(self, request):
        data = request.POST
        user = get_object_or_404(NewUser, email=data.get("email", None))
        confirm_user = get_object_or_404(Confirm_User, user=user)

        if confirm_user.valid_code(data.get("code", 0)) != True:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        if confirm_user.check_expired() != True:
            return Response(status=status.HTTP_403_FORBIDDEN)

        user = confirm_user.user
        user.is_active = True
        user.save()
        confirm_user.delete()

        return Response(f"Your account is now activated")


class Forget_Password(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Send Confirm code to email",
        parameters=[
            OpenApiParameter(
                name="email",
                type=OpenApiTypes.EMAIL,
                allow_blank=False,
            )
        ],
    )
    def get(self, reqeust):

        data = reqeust.data.copy()
        data["expire"] = Confirm_User.expire_time()
        data["code"] = Confirm_User.random_code()

        email_address = reqeust.GET.get("email", None)
        confrim_model = None
        try:
            user = NewUser.objects.get(email=email_address)
            data["user"] = user.pk
        except:
            return HttpResponse("invalid user")

        try:
            confrim_model = Confirm_User.objects.get(user=user)
        except:
            pass

        confirm = Serializer_Confirm_User(
            instance=confrim_model, data=data, partial=True
        )
        if confirm.is_valid(True):
            confirm = confirm.save()

        template = "forget_password.html"
        context = {"active_code": confirm.code, "domain": reqeust.META["HTTP_HOST"]}
        html_template = render_to_string(template, context)

        SendEmail(
            "درخواست تغییر رمز عبور",
            "کد احراز هویت شما {confirm.code} میباشد",
            [user.email],
            html_template,
        )

        return HttpResponse("check you email")

    @extend_schema(
        summary="Confirm activation code ",
        request={"application/x-www-form-urlencoded": Serializer_Confirm_Forget},
        responses={
            200: OpenApiTypes.STR,
            404: OpenApiTypes.OBJECT,
            403: OpenApiTypes.OBJECT,
            304: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request):
        data = request.POST
        user = get_object_or_404(NewUser, email=data.get("email", None))
        confirm_user = get_object_or_404(Confirm_User, user=user)

        # user = NewUser.objects.get(email=data.get('email', None))
        # confirm_user = Confirm_User.objects.get(user=user)

        if confirm_user.valid_code(data.get("code", 0)) != True:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        password1 = data.get("password", 0)
        password2 = data.get("password2", 1)
        if confirm_user.check_expired() != True:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if password1 != password2:
            return Response("Passwords Dosnt Match", status=status.HTTP_400_BAD_REQUEST)
        user = confirm_user.user
        user.set_password(password1)
        user.save()
        confirm_user.delete()
        return Response(f"password changed to {password1}")


class User_API(APIView):
    def get_permissions(self):
        method = self.request.method.lower()
        if method == "post":
            permission_classes = [
                permissions.AllowAny,
            ]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
            ]

        return [permission() for permission in permission_classes]

    def hash_password(self, password: str) -> str:
        hashed_password: str = make_password(password)
        return hashed_password

    @extend_schema(
        summary="Sing in new user",
        request=Serializer_User,
        responses={
            201: Serializer_User,
            400: OpenApiTypes.OBJECT,
        },
    )
    def post(self, requests) -> Union[Response, Http404]:
        data = requests.data
        serializer = Serializer_User(data=data)

        if serializer.is_valid(True):
            password: str = serializer.validated_data["password"]
            hashed_password = self.hash_password(password)
            user = serializer.save(password=hashed_password, is_active=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="User profile",
        responses={
            200: Serializer_User,
            # 400: OpenApiTypes.OBJECT,
        },
    )
    def get(self, reqeust) -> Response:
        serializer = Serializer_User(reqeust.user)
        return Response(serializer.data)

    @extend_schema(
        summary="Full update profile",
        request=Serializer_User,
        responses={
            200: Serializer_User,
            400: OpenApiTypes.OBJECT,
        },
    )
    def put(self, reqeust, **kwargs) -> Union[Response, Http404]:
        data = reqeust.data
        user = reqeust.user
        partial = kwargs.get("partial", False)
        serializser = Serializer_User(user, data, partial=partial)
        if serializser.is_valid(True):
            serializser.save()
            return Response(serializser.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Partial update profile",
        request=Serializer_User,
        responses={
            200: Serializer_User,
            400: OpenApiTypes.OBJECT,
        },
    )
    def patch(self, request):
        return self.put(request, partial=True)


def get_all_urls(reqeust):
    print(django_reverse(current_app="api"))
    return Response()


# class User(ViewSet):
#     def hash_password(self, password: str) -> str:
#         hashed_password: str = make_password(password)
#         return hashed_password

#     def list(self, request):
#         queryset = request.user
#         serializer = Serializer_User(queryset)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def create(self, request):
#         data = request.data
#         serializer = Serializer_User(data=data)

#         if serializer.is_valid(True):
#             password: str = serializer.validated_data["password"]
#             hashed_password = self.hash_password(password)
#             serializer.save(password=hashed_password)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def partial_update(self, request):
#         data = request.data
#         user = request.user
#         serializser = Serializer_User(user, data, partial=True)
#         if serializser.is_valid(True):
#             serializser.save()
#             return Response(serializser.data, status=status.HTTP_200_OK)

#     def update(self, request, pk=None):
#         data = request.data
#         user = request.user
#         serializser = Serializer_User(user, data, partial=True)
#         if serializser.is_valid(True):
#             serializser.save()
#             return Response(serializser.data, status=status.HTTP_200_OK)
