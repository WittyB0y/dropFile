# Generated by Django 4.1.7 on 2023-05-01 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_photo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(default='users/mainphoto/user.jpg', upload_to=''),
        ),
    ]
