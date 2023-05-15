from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class files(models.Model):
    slug = models.SlugField(null=False, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)
    updatedAt = models.DateTimeField(auto_now=True)
    downloded = models.IntegerField(default=0)
    seen = models.IntegerField(default=-1)
    configdata = models.TextField()
    ipdata = models.GenericIPAddressField()
    file = models.FileField(upload_to='media/')
    name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255)
    userid = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    access = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}, {self.createdAt.strftime("%H:%M %Y-%m-%d")}'


class renderData(models.Model):
    fileid = models.ManyToManyField(files)
    number = models.IntegerField(default=1)
    fileLink = models.CharField(max_length=500)


class FileAccess(models.Model):
    fileid = models.ForeignKey(files, on_delete=models.CASCADE, related_name='accesses')
    createdAt = models.DateTimeField(auto_now_add=True)
    existBefore = models.DateTimeField(null=True)
    seenUser = models.IntegerField(default=0)
    webSee = models.BooleanField(default=False)
    userSeeClient = models.BooleanField(default=True)
    amount = models.IntegerField(default=0)
    lookingSeeUsers = models.ManyToManyField(User, related_name='file_accesses')


class dataCounter(models.Model):
    allowedFiles = models.IntegerField(default=100, null=False)
    amount_of_files = models.IntegerField(default=0, null=False)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
