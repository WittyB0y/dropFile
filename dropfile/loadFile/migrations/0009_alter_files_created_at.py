# Generated by Django 3.2.16 on 2023-03-09 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loadFile', '0008_auto_20230309_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='created_at',
            field=models.BigIntegerField(default=1678404123.4510624),
        ),
    ]
