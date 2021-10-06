import json
from os import link
from sys import float_repr_style, version
from typing import Dict
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer,
    AsyncWebsocketConsumer,
)
from .models import Device
from channels.db import database_sync_to_async

# from asgiref.sync import sync_to_async
from channels.exceptions import StopConsumer
from WEB_SERVER.models import Source_Device
from AUTH_SYSTEM.models import Temp_link

# from channels.signals import
from django.urls import reverse
from django.contrib.sites.models import Site
from WEB_SERVER.utils import get_client_ip


def get_client_ip_2(headers):
    META = {}
    for key, value in dict(headers).items():

        META[key.decode("utf-8")] = value.decode("utf-8")
    x_forwarded_for = META.get('x-forwarded-for')
    x_real_real_ip = META.get('x-real-ip')
    if x_real_real_ip:

        ip = x_real_real_ip
    elif x_forwarded_for:
        print(x_forwarded_for)
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = META.get('remote-addr')
    return ip


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self, *args, **kwargs):
        headers = self.scope['headers']
        ip = get_client_ip_2(headers)
        print(ip)
        self.device = self.scope["device"]
        self.extra_header = self.scope["extra-header"]

        version = await self.valid_version(self.extra_header)
        if self.device is not None and version:

            await self.accept()
            print("Channel Name :", self.channel_name, "Token : ",
                  str(self.device.token))
            await self.channel_layer.group_add(str(self.device.token),
                                               self.channel_name)
            print("accept")
            await self.Change_status_device(True)
            exist_new_status = await self.Get_Command_Server()

            if exist_new_status:
                print("******************RUN*******************")
                await self.Change_Status_Command()
                await self.send_json(exist_new_status)

            print("***************DONE****************")

            status_update = await self.Check_update(version)
            if status_update == True:
                link_update = await self.Make_link("127.0.0.1")
                print(link_update)
                data = {"datatype": "update", "data": link_update}
                # data= json.dumps(data)
                # print(data)

                await self.send_json({
                    "datatype": "update",
                    "data": link_update
                })

        else:
            print("UnAccept")
            await self.close(
            )  # check device authentication in middleware and if not auth automatica reject request with error 403

    async def valid_version(self, extra_header: dict) -> bool:
        if "version" in extra_header:
            version = extra_header["version"]
            try:
                print(version)
                return float(version)
            except Exception as Error:
                print(Error)
                return False
        else:
            print("ELSE")
            return False

    @database_sync_to_async
    def Make_link(self, ip: str) -> str:
        temp_link = Temp_link(ip=ip, file=self.source.source)
        temp_link.save()
        domain = Site.objects.all()[0].domain
        app_url = reverse("UPDATE_LINK", args=(temp_link.link, ))
        full_url = fr"http://{domain}{app_url}"
        return full_url

    async def disconnect(self, code):
        try:
            await self.Change_status_device(False)
            await self.channel_layer.group_discard(str(self.device.token),
                                                   self.channel_name)
        except:
            pass
        raise StopConsumer(
        )  # rise an error for stop and close socket connection

    @database_sync_to_async
    def Check_update(self, version: float):
        device_type = self.device.type
        try:
            self.source = Source_Device.objects.get(type=device_type)
            return not (
                self.source.version <= version
            )  # check if version lower from source.version return True
        except Source_Device.DoesNotExist:
            return False

    @database_sync_to_async
    def Change_status_device(self, status=False):
        self.scope["device"].status = status
        self.scope["device"].save()

    @database_sync_to_async
    def Change_Status_Command(self):
        self.scope["device"].Command_Device.complated = True
        self.scope["device"].Command_Device.save()
        print("Status Changed")

    @database_sync_to_async
    def Get_Command_Server(self):  # get the last command from server to device
        device = self.scope["device"]
        try:
            if device.Command_Device.complated != True:
                return device.Command_Device.data
            else:
                return False
        except:  # dont exist any command from server its rise an error
            return False

    @database_sync_to_async
    def Save_status(self, status):
        self.scope["device"].Data_Device.create(data=status)

    async def Command(self, event):
        data = event["data"]
        await self.send_json(data)
        await self.Change_Status_Command()
        await self.Save_status(data)
        print("Running", event["data"])

    async def receive_json(self, content):
        # Ngative = lambda data : 'OFF' if data == 'ON' else 'ON'
        # await self.send('{"statusled":["OFF","OFF","OFF","OFF"]}')
        print(f">>Before>>> {content }")
        # content['statusled'] = list(map(Ngative,content['statusled']))
        # data = content

        # await self.send_json(content)
        # print(f'>>After>>> {content }')
