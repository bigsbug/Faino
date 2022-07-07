from django.apps import AppConfig
from django.db import IntegrityError, OperationalError


def Create_Permissinos():
    from faino.AuthSystem.models import Endpoints
    from faino.API.views import Device_API

    list_funcation = []
    for key, value in Device_API.__dict__.items():
        if callable(value):
            list_funcation.append(key)
            try:
                Endpoints.objects.get(name=key, app_name="API", class_name="Device")
            except:
                Endpoints(name=key, app_name="API", class_name="Device").save()

    # Remove not found endpoints
    for item in Endpoints.objects.filter(app_name="API", class_name="Device"):

        if item.name not in list_funcation:
            print(item.name)
            item.delete()


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "faino.API"

    def ready(self):
        from faino.AuthSystem.models import Endpoints, PermissionGroup

        try:
            Create_Permissinos()
        except OperationalError as Error:
            print(f"Error : {Error}")

        try:  # make default permission group for owner users
            Owner_group = PermissionGroup(name="owner")
            Owner_group.save()
            permissions = Endpoints.objects.all()
            Owner_group.permissions.set(permissions)
            DEFAULT_TYPE = Owner_group.save()
        except IntegrityError:
            ...
