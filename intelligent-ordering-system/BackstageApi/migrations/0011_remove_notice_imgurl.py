# Generated by Django 4.2 on 2023-04-16 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BackstageApi', '0010_rename_notice_url_notice_imgurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='imgURL',
        ),
    ]
