from pkgutil import iter_modules
from django.apps import AppConfig
from django.db import IntegrityError, OperationalError


def Create_Permissinos():
    from faino.AuthSystem.models import Permissions
    from faino.WebServer.api_v1.views import Device_API

    list_funcation = []
    for key, value in Device_API.__dict__.items():
        if callable(value):
            list_funcation.append(key)
            try:
                Permissions.objects.get(
                    name=key, app_name="WebServer", class_name="Device"
                )
            except:
                Permissions(name=key, app_name="WebServer", class_name="Device").save()

    for item in Permissions.objects.filter(app_name="WebServer", class_name="Device"):

        # print(f"{item.name}  {(item.name not in list_funcation)}")
        if item.name not in list_funcation:
            print(item.name)
            item.delete()


class WebServerppConfig(AppConfig):
    name = "faino.WebServer"

    def ready(self):
        from faino.AuthSystem.models import Permissions, Permissions_Group
        from faino.WebServer import signals

        # try:
        #     Create_Permissinos()
        # except OperationalError as Error:
        #     print(f"Error : {Error}")

        # try:  # make default permission group for owner users
        #     Owner_group = Permissions_Group(name="owner")
        #     Owner_group.save()
        #     permissions = Permissions.objects.all()
        #     Owner_group.permissions.set(permissions)
        #     DEFAULT_TYPE = Owner_group.save()
        # except IntegrityError:
        #     pass
