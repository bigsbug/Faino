from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.http.response import HttpResponseNotAllowed
from .models import Device


class TokenAuth_middleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, *args):

        headers = dict(scope["headers"])

        try:
            # print(headers)
            Token = headers[b"token"].decode()
            device = await self.ChackToken(Token)
            scope["device"] = device
            return await self.inner(scope, *args)

        except Exception as Error:
            # print(f"Error : {Error}\n"+'*'*10)
            scope["device"] = None
            return await self.inner(scope, *args)

    @database_sync_to_async
    def ChackToken(self, Token):
        try:  # try if exist a device with same token return a object of that
            device = Device.objects.get(token=Token)
            print("Valid Token")
            return device
        except:

            print("invalid Token")
            # pass the error to consumers and if call method self.close() returned this error
            return HttpResponseNotAllowed()


MiddleWareStack_authToken = lambda inner: TokenAuth_middleware(
    AuthMiddlewareStack(inner)
)
