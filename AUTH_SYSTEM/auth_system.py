
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import check_password, make_password
from AUTH_SYSTEM.models import New_User
from django.http import HttpRequest
from typing import Optional, Any


class Custom_User_BackendModel(BaseBackend):
    def authenticate(self, request: HttpRequest, username: Optional[str], password: Optional[str], **kwargs: Any) -> Optional[AbstractBaseUser]:
        try:
            hashed_password = make_password(password,)
            User: New_User = New_User.objects.get(
                username=username)
            print('USER EXiST')
            if check_password(hashed_password, User.password):
                return User
            else:
                print(hashed_password)
                print(User.password)
                print('password incorrent')
                return None
        except New_User.DoesNotExist:
            return None

        except New_User.DoesNotExist:
            return None

    def get_user(self, user_id: int) -> Optional[AbstractBaseUser]:
        try:
            User: New_User = New_User.objects.get(user_id)
            return User
        except New_User.DoesNotExist:
            return None
