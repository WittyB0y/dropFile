# Generated by Django 3.2.16 on 2023-03-09 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loadFile', '0009_alter_files_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
