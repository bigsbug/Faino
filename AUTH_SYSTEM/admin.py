from django.contrib import admin
from AUTH_SYSTEM.models import New_User, Temp_link, Confirm_User


class USER_ADMIN(admin.ModelAdmin):
    list_display = [
        'username',
        'is_active',
        'is_staff',
        "first_name",
        "last_name",
        "email",
        "phone",
    ]


class TEMP_LINK_ADMIN(admin.ModelAdmin):
    list_display = [
        'link',
        'expire',
    ]


class CONFIRM_USER_ADMIN(admin.ModelAdmin):
    list_display = [
        'token',
        'expire',
        'code',
    ]


admin.site.register(New_User, USER_ADMIN)
admin.site.register(Temp_link, TEMP_LINK_ADMIN)
admin.site.register(Confirm_User, CONFIRM_USER_ADMIN)
