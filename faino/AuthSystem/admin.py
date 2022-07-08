import imp
from django.contrib import admin
from faino.AuthSystem.models import (
    NewUser,
    TempLink,
    UserConfirm,
    Endpoint,
    Permission,
)
from faino.AuthSystem.froms import Permissions_Grup_FORM


class USER_ADMIN(admin.ModelAdmin):
    list_display = [
        "username",
        "is_active",
        "is_staff",
        "first_name",
        "last_name",
        "email",
        "phone",
    ]


class TEMP_LINK_ADMIN(admin.ModelAdmin):
    list_display = [
        "link",
        "expire",
    ]


class CONFIRM_USER_ADMIN(admin.ModelAdmin):
    list_display = [
        "token",
        "expire",
        "code",
    ]


class Permissions_Group_REGISTER(admin.ModelAdmin):
    list_display = ["name"]
    form = Permissions_Grup_FORM


admin.site.register(NewUser, USER_ADMIN)
admin.site.register(TempLink, TEMP_LINK_ADMIN)
admin.site.register(UserConfirm, CONFIRM_USER_ADMIN)
admin.site.register(Permission, Permissions_Group_REGISTER)
