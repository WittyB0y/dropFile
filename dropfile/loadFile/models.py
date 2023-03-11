from django.db import models
from django.contrib.auth.models import User


class files(models.Model):
    slug = models.SlugField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    downloded = models.IntegerField(default=0)
    seen = models.IntegerField(default=-1)
    configdata = models.TextField()
    ipdata = models.GenericIPAddressField()
    file = models.FileField(upload_to='media/')
    name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255)
    userid = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    access=models.BooleanField(default=False)
