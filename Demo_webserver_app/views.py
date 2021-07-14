from time import time
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse, JsonResponse,Http404

from django.shortcuts import render , get_object_or_404,get_list_or_404

from django.views import View
from django.views.decorators.csrf import csrf_exempt

from rest_framework import permissions
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (Device, 
                    Profile,
                    Type,
                    NewStatus,
                    Data)

from .serializer import (Serializer_Device_Data, Serializer_NewStatus,
                         Serializer_User, Serializer_Device,
                         Serializer_Profile, Serializer_Get_NewStatus)


def Filter_Device(data,user):

    if 'token' in data:
        try:

            data = get_object_or_404( Device,token=data['token'],user=user)

        except:
            raise Http404("token is not valid")
        return data
    
    else:

        if 'type' in data:

            try:
                NameType = get_object_or_404(Type,name=data['type'])
                return get_list_or_404(Device,type = NameType,user=user)
            except:
                raise Http404()

        else:
            raise Http404()



def index(request):
    return HttpResponse('Your Connected to WebServer')

class Get_Device(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        device = get_list_or_404(Device,user=request.user)
        data = Serializer_Device(device,many=True).data
        return Response(data)

    def post(self,request):
        data = request.data

        device = Filter_Device(data,request.user)

        if 'type' in data: # if "type" were in Request.data it's necessary to use flag many = True because needs get a list of instances
            serial_data = Serializer_Device(device,many=True).data
        elif 'token' in data:
            serial_data = Serializer_Device(device).data
        else:
            raise Http404
        return Response(serial_data)

class Get_Data(APIView):

    def post(self,request):
        user = request.user
        token = request.data['token']
        # if Serializer_Device(data=request.data).is_valid():
        device = get_object_or_404(Device,user=user,token=token)
        print(device)
        data_instance = get_list_or_404(Data,device=device)
        serializer = Serializer_Device_Data(data_instance,many=True)
        return Response(serializer.data)
        # else:
        #     print('NOT‌ Valid UUID4')
        #     return Response(status=status.HTTP_400_BAD_REQUEST)


class Get_Info_User(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        user = request.user
        serializer = Serializer_User(user)
        return Response(serializer.data)
    
class Set_NewStatus(APIView):
    def post(self,request):
        data = request.data
        token = data['token']
        data_NewStatus = {'data':data['data'],'complated':data['complated']}

        serializer = Serializer_Get_NewStatus(data=data)

        if serializer.is_valid(raise_exception=True):

            device = get_object_or_404(Device,user= request.user,token=token)
            serializer = Serializer_NewStatus(data=data_NewStatus)
            if serializer.is_valid():
                serializer.save(device = device)

                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response() 

