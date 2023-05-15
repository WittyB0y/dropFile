from django.db import models


class news(models.Model):
    title = models.CharField(max_length=20)
    text = models.TextField(max_length=200)
    link = models.CharField(max_length=170)
    image = models.CharField(max_length=170)
