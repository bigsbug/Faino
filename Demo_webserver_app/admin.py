from django.contrib import admin
from Demo_webserver_app.models import Device,Profile,Data,NewStatus

class Device_Register(admin.ModelAdmin):
    list_display = ['name','token',"status"]

admin.site.register(Device,Device_Register)
admin.site.register(Data)
admin.site.register(Profile)
admin.site.register(NewStatus)
