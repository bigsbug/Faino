import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NameProject.settings")

import django

django.setup()

from django.core.management import call_command

from channels.layers import get_channel_layer

channel_layer = get_channel_layer()
from asgiref.sync import async_to_sync


group = "test"

async_to_sync(channel_layer.send)(
    group,
    {
        "type": "funcname",
    },
)
