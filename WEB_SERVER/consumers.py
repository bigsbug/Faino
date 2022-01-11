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
    for key, item in META.items():
        print(f"{key} : {item}")
    x_forwarded_for = META.get("x-forwarded-for")
    x_real_real_ip = META.get("x-real-ip")
    if x_real_real_ip:

        ip = x_real_real_ip
    elif x_forwarded_for:
        print(x_forwarded_for)
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = META.get("remote-addr")
    return ip


class Device_WB(AsyncJsonWebsocketConsumer):
    async def connect(self, *args, **kwargs):

        headers = self.scope["headers"]
        version = self.scope["version"]
        print(version)
        self.device = self.scope["device"]
        ip = get_client_ip_2(headers)
        print(ip)
        # self.device = self.scope["device"]
        # self.extra_header = self.scope["extra-header"]

        if self.device is not None:

            await self.accept()
            print(
                "Channel Name :", self.channel_name, "Token : ", str(self.device.token)
            )
            await self.channel_layer.group_add(
                str(self.device.token), self.channel_name
            )
            print("accept")
            await self.Change_status_device(True)
            new_command = await self.Get_Command_Server()

            if new_command:
                print("******************RUN*******************")
                for command in new_command:
                    # print(command.command)
                    await self.send_json(command.command)
                    print('Command Sended To Device.')
                    await self.Change_Status_Command(command)
                    

            print("***************DONE****************")

            status_update = await self.Check_update(version)
            if status_update == True:
                link_update = await self.Make_link(ip)
                # print(link_update)
                data = {"datatype": "update", "data": link_update}

                # data= json.dumps(data)
                print(data)

                await self.send_json(data)

        else:
            print("UnAccept")
            await self.close()  # check device authentication in middleware and if not auth automatica reject request with error 403

    @database_sync_to_async
    def Make_link(self, ip: str) -> str:
        temp_link = Temp_link(ip=ip, file=self.source.source)
        temp_link.save()
        domain = Site.objects.all()[0].domain
        app_url = reverse("WEBSERVER:UPDATE_LINK", args=(temp_link.link,))
        full_url = fr"http:/1/{domain}{app_url}"
        return full_url

    async def disconnect(self, code):
        try:
            await self.Change_status_device(False)
            await self.channel_layer.group_discard(
                str(self.device.token), self.channel_name
            )
        except:
            pass
        raise StopConsumer()  # rise an error for stop and close socket connection

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
    def Change_Status_Command(self,command):
            command.status =True
            command.save()
            print("Status Changed")

    @database_sync_to_async
    def Get_Command_Server(self,id=None):  # get all commands or one for Device 
        device = self.scope["device"]
        try:
            if id ==None:
                
                data = device.Command_Device.filter(status=False)
                
                if data:
                    return data
                else:
                    return False
                
            else:
                return device.Command_Device.get(pk=id)
            
        except:  # dont exist any command from server its rise an error
            return False

    @database_sync_to_async
    def Save_status(self, status):
        self.scope["device"].Data_Device.create(data=status)

    async def Command(self, event):
                  
        command = await self.Get_Command_Server(id = event["command"])

        await self.send_json(command.command)
        await self.Change_Status_Command(command)
        await self.Save_status(command.command)
        
        print("Running",command.command)

    async def receive_json(self, content):
        print(f">>Before>>> {content }")
