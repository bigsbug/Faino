import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer,AsyncWebsocketConsumer
from .models import Device
from channels.db import database_sync_to_async
# from asgiref.sync import sync_to_async
from channels.exceptions import StopConsumer
# from channels.signals import  

class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self): 
        device = self.scope['device']

        if device is not None: 

            await self.accept()
            print('Channel Name :',self.channel_name,"Token : ",str(device.token))
            await self.channel_layer.group_add(str(device.token),self.channel_name)
            print('accept')
            await self.Change_status_device(True)
            exist_new_status = await self.Get_NewStatus_server()

            if exist_new_status:
                print('******************RUN*******************')
                await self.Change_status_command()
                await self.send_json(exist_new_status)

            print('***************DONE****************')
    
        else:
            print('UnAccept')
            await self.close() # check device authentication in middleware and if not auth automatica reject request with error 403


    async def disconnect(self,code):
        try:
            await self.Change_status_device(False)
            await self.channel_layer.group_discard(str(device.token),self.channel_name)
        except:
            pass
        raise StopConsumer() # rise an error for stop and close socket connection

    @database_sync_to_async
    def Change_status_device(self,status = False):
        self.scope['device'].status = status
        self.scope['device'].save()

    @database_sync_to_async
    def Change_status_command(self):
        self.scope['device'].New_Status_Device.complated = True
        self.scope['device'].New_Status_Device.save()
        print('Status Changed')

    @database_sync_to_async
    def Get_NewStatus_server(self): # get the last command from server to device
        device = self.scope['device']
        try:
            if device.New_Status_Device.complated != True:
                return device.New_Status_Device.data
            else:
                return False
        except: # dont exist any command from server its rise an error
            return False
    @database_sync_to_async
    def Save_status(self,status):
        self.scope['device'].Data_Device.create(data=status)


    async def Send_NewStatus(self,event):
        data = event['data']
        await self.send_json(data)
        await self.Change_status_command()
        await self.Save_status(data)
        print('Running',event['data'])

    async def receive_json(self, content):
        Ngative = lambda data : 'OFF' if data == 'ON' else 'ON'
        # await self.send('{"statusled":["OFF","OFF","OFF","OFF"]}')
        print(f'>>Before>>> {content }')
        # content['statusled'] = list(map(Ngative,content['statusled']))
        # data = content
        
        # await self.send_json(content)
        # print(f'>>After>>> {content }')
