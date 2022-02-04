from pkgutil import iter_modules
from django.apps import AppConfig
from django.db import OperationalError


def Create_Permissinos():
    from AUTH_SYSTEM.models import Permissions
    from WEB_SERVER.api_v1.views import Device_API
    list_funcation = []
    for key, value in Device_API.__dict__.items():
        if callable(value):
            list_funcation.append(key)
            try:
                Permissions.objects.get(name=key, app_name="WEB_SERVER",
                                        class_name="Device")
            except:
                Permissions(name=key, app_name="WEB_SERVER",
                            class_name="Device").save()

    for item in Permissions.objects.filter(
            app_name='WEB_SERVER', class_name='Device'):

        # print(f"{item.name}  {(item.name not in list_funcation)}")
        if item.name not in list_funcation:
            print(item.name)
            item.delete()


class CoreAppConfig(AppConfig):
    name = "WEB_SERVER"

    def ready(self):
        from WEB_SERVER import signals
        try:
            Create_Permissinos()
        except OperationalError as Error:
            print(f"Error : {Error}")
