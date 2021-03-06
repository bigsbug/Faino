from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from faino.WebServer.models import Command
from django.db.models.query import exceptions as Er

# @receiver(pre_save, sender=Command)
# def Delete_last_command(
#         sender, instance,
#         **kwargs):  # if exist a command delete the last command
#     try:
#         status = Command.objects.get(device=instance.device)
#         status.delete()
#         print("Remove last command.")
#     except Er.ObjectDoesNotExist as Error:
#         print("set a new command")


@receiver(post_save, sender=Command)
def Send_command_to_device(sender, instance, created, **kwargs):
    if instance.status == False:
        channels_layer = get_channel_layer()
        name_group = str(instance.device.pk)
        command = {"type": "Command", "command": instance.pk}
        async_to_sync(channels_layer.group_send)(name_group, command)
        # print("Send singal to consumers")
