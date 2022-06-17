from django.apps import AppConfig


class AuthSystemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "faino.AuthSystem"

    def ready(self):
        from faino.AuthSystem import signals
