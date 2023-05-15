from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


class photo(models.Model):
    userid = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="media/", default="media/users/mainphoto/user.jpg")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        photo.objects.create(userid=instance)
