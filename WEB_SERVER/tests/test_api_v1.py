from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from WEB_SERVER.models import Device, Command, Data, Button
from WEB_SERVER.serializer import (
    Serializer_Device,
    Serializer_Command,
    Serializer_Device_Data,
    Serializer_Buttons,
)

# from rest_framework.reverse import reverse
from django.urls import reverse
from AUTH_SYSTEM.models import New_User as User
from WEB_SERVER.api_v1.views import Device as Device_API
from WEB_SERVER.api_v1.urls import Router


class ApiTestCase(APITestCase):
    fixtures = ["ApiDB_fixture", "user"]

    def setUp(self) -> None:
        self.username = "nova"
        self.password = "novaman"
        self.user = User.objects.all()[0]
        token_ul = reverse("token_pair")
        pyload = {"username": self.username, "password": self.password}
        token = self.client.post(token_ul, pyload, "json")
        self.token = token.data["access"]
        self.pk = "da908b69-00d9-42d7-8d2b-cba5009b76bf"

        return super().setUp()

    ########################################################
    #                  Device TestCase                     #
    ########################################################

    def test_get_all_device_of_user(self):

        url = reverse("WEBSERVER:Device-list")  # '/api/devices/'
        # url = Device_API().reverse_action('list')
        url = "/api/devices/"
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.get(url)
        device = Device.objects.filter(user=self.user)
        all_device = Serializer_Device(device, many=True)
        self.assertEqual(response.data, all_device.data)

    def test_make_new_device(self):
        url = reverse("WEBSERVER:Device-list")  # '/api/device/'
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        data = {
            "name": "New Device",
            "type": "Light",
            "ip": "127.0.0.1",
            "password": "new password",
            "mac": "138.0.1.87",
            "description": "test description",
            "user": self.user,
            "status": True,
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_retrieve_device(self):

        url = reverse("WEBSERVER:Device-list") + self.pk + "/"  # '/api/device/pk'

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.get(url)

        self.assertEqual(response.status_code, 200)

        device = Device.objects.get(token=self.pk)
        device = Serializer_Device(device)

        self.assertEqual(response.data, device.data)

    def test_retrieve_device_by_type(self):
        type_deivce = "Light"
        url = reverse(
            "WEBSERVER:Device-filter_type",
            args=[
                type_deivce,
            ],
        )

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        device = Device.objects.filter(user=self.user, type=type_deivce)
        device = Serializer_Device(device, many=True)
        self.assertEqual(response.data, device.data)

    def test_update_device(self):
        url = reverse("WEBSERVER:Device-list") + self.pk + "/"  # '/api/device/pk'
        data = {
            "name": "New Name",
            "type": "Light",
            "ip": "127.0.0.1",
            "password": "new password",
            "mac": "138.0.1.87",
            "description": "test description",
            "user": self.user,
            "status": True,
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.put(url, data)
        self.assertEqual(response.status_code, 200)

        device = Device.objects.get(token=self.pk)
        device = Serializer_Device(device)

        self.assertEqual(response.data, device.data)

    def test_partial_update_device(self):
        url = reverse("WEBSERVER:Device-list") + self.pk + "/"  # '/api/device/pk'
        data = {
            "name": "New Name 2",
            "type": "Light",
            "ip": "127.0.0.99",
            "password": "new password 2",
            # "mac": "138.0.1.87",
            # "description": "test description",
            # "user": self.user,
            # "status": True,
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.patch(url, data)
        self.assertEqual(response.status_code, 200)

        device = Device.objects.get(token=self.pk)
        device = Serializer_Device(device)

        self.assertEqual(response.data, device.data)

    def test_destory_device(self):

        url = reverse("WEBSERVER:Device-list") + self.pk + "/"  # '/api/device/pk'

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.delete(url)

        self.assertEqual(response.status_code, 204)

    ########################################################
    #                    Data TestCase                     #
    ########################################################

    def test_get_all_data_of_device(self):
        url = reverse(
            "WEBSERVER:Device-data",
            args=[
                self.pk,
            ],
        )
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_all_data_of_device_without_exist_data(self):
        pk = "acf8d707-2127-447a-9821-7d30ef0b0c9a"
        url = reverse(
            "WEBSERVER:Device-data",
            args=[
                pk,
            ],
        )
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.get(url)
        self.assertEqual(response.status_code, 404)

    ########################################################
    #                 Command TestCase                     #
    ########################################################

    def test_get_last_command(self):
        url = reverse(
            "WEBSERVER:Device-command",
            args=[
                self.pk,
            ],
        )
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_make_new_command(self):
        url = reverse(
            "WEBSERVER:Device-command",
            args=[
                self.pk,
            ],
        )
        data = {
            "data": {"destroy": "YES"},
            "complated": False,
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.post(url, data, "json")
        self.assertEqual(response.status_code, 201)

        command_instanse = Command.objects.get(device=self.pk)  # last added Command
        command = Serializer_Command(command_instanse)
        self.assertEqual(response.data, command.data)

    ########################################################
    #                  Button TestCase                     #
    ########################################################

    def test_get_all_buttons_of_device(self):
        url = reverse(
            "WEBSERVER:Device-button",
            args=[
                self.pk,
            ],
        )
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_make_new_button(self):
        url = reverse("WEBSERVER:Device-button", args=[self.pk])
        data = {
            "control_name": "Cooler",
            "name": "UP",
            "is_star": False,
            "array": "array UP Button IR ",
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.post(url, data)
        self.assertEqual(response.status_code, 200)
        button = Button.objects.filter(device=self.pk).last()
        button = Serializer_Buttons(button)
        self.assertEqual(button.data, response.data)

    def test_retrieve_button_of_device(self):
        button = Button.objects.filter(device=self.pk).last()
        url = reverse("WEBSERVER:Device-button_retrieve", args=[self.pk, button.pk])
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        button = Serializer_Buttons(button)
        self.assertEqual(button.data, response.data)

    def test_destory_button(self):
        button = Button.objects.filter(device=self.pk).last()
        url = reverse("WEBSERVER:Device-button_retrieve", args=[self.pk, button.pk])
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_update_button(self):
        button = Button.objects.filter(device=self.pk).last()
        url = reverse("WEBSERVER:Device-button_retrieve", args=[self.pk, button.pk])
        data = {
            "control_name": "Change Name Control to Hoode",
            "name": "UP",
            "is_star": False,
            "array": "array UP Button IR ",
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.put(url, data)
        self.assertEqual(response.status_code, 200)
        button = Button.objects.filter(device=self.pk).last()
        button = Serializer_Buttons(button)
        self.assertEqual(button.data, response.data)

    def test_partial_update_button(self):
        button = Button.objects.filter(device=self.pk).last()
        url = reverse("WEBSERVER:Device-button_retrieve", args=[self.pk, button.pk])
        data = {
            "control_name": "Change Name Control to Hoode",
            # 'name': 'UP',
            # 'is_star': False,
            # 'array': 'array UP Button IR '
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        button = Button.objects.filter(device=self.pk).last()
        button = Serializer_Buttons(button)
        self.assertEqual(button.data, response.data)
