# Generated by Django 4.1.7 on 2023-04-28 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='time_created',
        ),
    ]
