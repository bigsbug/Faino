from django.contrib import admin
from Demo_webserver_app.models import ( Device,
                                        Profile,
                                        Data,
                                        NewStatus,
                                        Type
                                        )

class Device_Register(admin.ModelAdmin):
    list_display = ['name','token',"status"]

class Data_Register(admin.ModelAdmin):
    list_display = ['device','date','data']

class NewStatus_Register(admin.ModelAdmin):
    list_display = ['device','date','complated','data']

admin.site.register(Device,Device_Register)
admin.site.register(Data,Data_Register)
admin.site.register(NewStatus,NewStatus_Register)
admin.site.register(Profile)
admin.site.register(Type)