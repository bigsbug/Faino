from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db.models.query import exceptions as Er
from django.contrib.auth.models import User

# from AUTH_SYSTEM.models import Profile

# @receiver(post_save, sender=User)
# def Create_new_profile(sender, instance, created, **kwargs):

#     if created:

#         Profile.objects.create(user=instance, name=instance.username)

#     else:

#         try:

#             Profile.objects.get(user=instance)

#         except Er.ObjectDoesNotExist as Error:

#             Profile.objects.create(user=instance, name=instance.username)
