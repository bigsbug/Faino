from django.apps import AppConfig


class AuthSystemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "AUTH_SYSTEM"

    def ready(self):
        from AUTH_SYSTEM import signals
