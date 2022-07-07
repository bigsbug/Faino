import imp
from django.contrib import admin
from faino.AuthSystem.models import (
    NewUser,
    Temp_link,
    Confirm_User,
    Permissions,
    Permissions_Group,
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
admin.site.register(Temp_link, TEMP_LINK_ADMIN)
admin.site.register(Confirm_User, CONFIRM_USER_ADMIN)
admin.site.register(Permissions_Group, Permissions_Group_REGISTER)
