# Generated by Django 3.2.16 on 2023-03-09 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loadFile', '0007_files_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='access',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='files',
            name='created_at',
            field=models.DateTimeField(default=1678403537.455855),
        ),
    ]