from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class idPhone(models.Model):
    userid = models.OneToOneField(User, on_delete=models.CASCADE)
    devid = models.CharField(max_length=100, null=True)


@receiver(post_save, sender=User)
def create_device_id(sender, instance, created, **kwargs):
    if created:
        print(instance)
        idPhone.objects.create(userid=instance)
