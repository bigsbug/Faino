from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.http.response import HttpResponseBadRequest
from .models import Device
import base64
import json


class TokenAuth_middleware:
    def __init__(self, inner, *args):
        self.inner = inner

    async def __call__(self, scope, *args):

        headers = dict(scope["headers"])
        if b"extra-header" not in headers:
            print("cant find ExtraHeader in headers")
            return HttpResponseBadRequest

        # try:
        try:
            encoded_value = headers[b"extra-header"]
            extra_header = base64.b64decode(encoded_value)
            extra_header = json.loads(extra_header.lower())

            device = await self.CheckToken(extra_header["token"])
        except:
            return HttpResponseBadRequest

        if (
            "version" not in extra_header and "token" not in extra_header
        ):  # check "Version" & "Token" exist in Json
            print("cant find version or token in ExtrHeader")
            return HttpResponseBadRequest

        scope["device"] = device
        scope["version"] = float(extra_header["version"])

        return await self.inner(scope, *args)

        # except Exception as Error:
        #     print(f"Error : {Error}\n" + '*' * 10)
        #     scope["device"] = None
        #     return await self.inner(scope, *args)

    @database_sync_to_async
    def CheckToken(self, Token):
        try:  # try if exist a device with same token return a object of that
            device = Device.objects.get(token=Token)
            print("Valid Token")
            return device
        except:

            print("invalid Token")
            # pass the error to consumers and if call method self.close() returned this error
            return HttpResponseBadRequest


MiddleWareStack_authToken = lambda inner: TokenAuth_middleware(
    AuthMiddlewareStack(inner)
)
