from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from Demo_webserver_app.models import Device, Profile,NewStatus
from django.db.models.query import exceptions as Er
from django.contrib.auth.models import User

@receiver(post_save,sender=User)
def Create_new_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance,name=instance.username)
    else:
        try:
            Profile.objects.get(user=instance)
        except Er.ObjectDoesNotExist as Error :
            Profile.objects.create(user=instance,name=instance.username) 
        print('Profile User updated')

@receiver(pre_save,sender=NewStatus)
def Delete_last_command(sender,instance,**kwargs):#if exist a command delete the last command 
    try:
        status = NewStatus.objects.get(device=instance.device)
        status.delete()
        print('the last sataus deleted.')
    except Er.ObjectDoesNotExist as Error :
        print('set a new status')
        
@receiver(post_save,sender=NewStatus)
def Send_status_to_device(sender,instance,**kwargs):
    if instance.complated == False:
        channels_layer = get_channel_layer()
        name_group = str(instance.device.pk)
        data = instance.data
        command = {'type':'Send_NewStatus','data':data}
        async_to_sync(channels_layer.group_send)(name_group,command)
        print('send singal to consumers')