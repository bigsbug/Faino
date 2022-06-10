import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Core.settings")

import django

django.setup()

from django.core.management import call_command

from channels.layers import get_channel_layer

channel_layer = get_channel_layer()
from asgiref.sync import async_to_sync

# group = "9f6aada7-9cd5-4a45-bef6-41432dc5bc1f"
group = "test"

async_to_sync(channel_layer.send)(
    "specific..inmemory!VtHNxObamqMs",
    {
        "type": "NewStatus",
    },
)
# >>> from channels.layers import get_channel_layer
# >>> from asgiref.sync import async_to_sync
# >>> channel_layer = get_channel_layer()
# >>> async_to_sync(channel_layer.group_send)('test123', {'type': 'event.message'})
# >>> group = "9f6aada7-9cd5-4a45-bef6-41432dc5bc1f"
# >>> async_to_sync(channel_layer.group_send)('test',{"type": "NewStatus","data":'"statusled":["OFF","OFF","OFF","OFF"]' })

print("Done")
