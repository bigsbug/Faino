from django.contrib import admin
from WEB_SERVER.models import Device, Data, Command, Source_Device, Type, Button


class Device_Register(admin.ModelAdmin):
    list_display = ["name", 'type', "token", "status"]
    list_filter = ['status', 'type']


class Data_Register(admin.ModelAdmin):
    list_display = ["device", "date", "data"]


class Command_Register(admin.ModelAdmin):
    list_display = ["device","type", "date", "status", "command"]


class Button_Register(admin.ModelAdmin):
    list_display = ["device", "control_name", "name", "is_star"]


admin.site.register(Device, Device_Register)
admin.site.register(Data, Data_Register)
admin.site.register(Command, Command_Register)
admin.site.register(Type)
admin.site.register(Source_Device)
admin.site.register(Button, Button_Register)
