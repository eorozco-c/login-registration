# Generated by Django 2.2.4 on 2021-08-12 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_login', '0002_user_birthday'),
        ('app_wall', '0002_auto_20210812_0112'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cooment',
            new_name='Comment',
        ),
    ]