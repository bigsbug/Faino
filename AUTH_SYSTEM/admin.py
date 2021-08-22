from django.contrib import admin
from AUTH_SYSTEM.models import New_User


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


admin.site.register(New_User, USER_ADMIN)
