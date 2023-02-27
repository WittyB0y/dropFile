from django.db import models
from django.contrib.auth.models import User


class photo(models.Model):
    userid = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="users/mainphoto/", default="users/mainphoto/user.jpg")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

