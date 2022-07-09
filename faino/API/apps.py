from django.apps import AppConfig
from django.db import IntegrityError, OperationalError


def Create_Permissinos():
    from faino.AuthSystem.models import Endpoint
    from faino.API.views import Device_API

    list_funcation = []
    for key, value in Device_API.__dict__.items():
        if callable(value):
            list_funcation.append(key)
            try:
                Endpoint.objects.get(name=key, app_name="API", class_name="Device")
            except:
                Endpoint(name=key, app_name="API", class_name="Device").save()

    # Remove not found endpoints
    for item in Endpoint.objects.filter(app_name="API", class_name="Device"):

        if item.name not in list_funcation:
            print(item.name)
            item.delete()


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "faino.API"

    def ready(self):
        from faino.AuthSystem.models import Endpoint, Permission

        try:
            Create_Permissinos()
        except OperationalError as Error:
            print(f"Error : {Error}")

        try:  # make default permission group for owner users
            Owner_group = Permission(name="owner")
            Owner_group.save()
            endpoints = Endpoint.objects.all()
            Owner_group.endpoints.set(endpoints)
            DEFAULT_TYPE = Owner_group.save()
        except IntegrityError:
            ...
