# Generated by Django 4.2 on 2023-04-10 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ForegroundApi', '0002_dish_alter_user_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='integral',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
    ]
