# Generated by Django 4.1.7 on 2023-02-19 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loadFile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='downloded',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='files',
            name='seen',
            field=models.IntegerField(default=-1),
        ),
    ]
