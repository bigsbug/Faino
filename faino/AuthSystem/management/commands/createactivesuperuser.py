from getpass import getpass

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from faino.AuthSystem.models import New_User


class Command(BaseCommand):

    help = "Create an active super user"

    def handle(self, *args, **options):
        username = input("Username : ")
        email = input("Email : ")
        phone = input("Number Phone : ")

        while True:
            password = getpass("Password : ")
            password2 = getpass("Enter Password Again : ")
            if password != password2:
                self.stdout.write(self.style.NOTICE("Passwords not same"))
            else:
                break

        try:
            user = New_User(username=username, phone=phone, email=email)
            user.set_password(password)
            user.is_active = True
            user.is_superuser = True
            user.is_staff = True
            user.full_clean()
            user.save()

            self.stdout.write(self.style.SUCCESS("Super User Crated"))

        except ValidationError as Error:
            for key, value in Error.message_dict.items():
                self.stdout.write(self.style.ERROR(f"{key} : {value}"))
        except Exception as Error:
            self.stdout.write(self.style.ERROR(Error))
