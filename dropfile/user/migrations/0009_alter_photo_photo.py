# Generated by Django 4.1.7 on 2023-05-15 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_photo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(default='media/users/mainphoto/user.jpg', upload_to='media/'),
        ),
    ]
