# Generated by Django 4.2 on 2023-04-14 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ForegroundApi', '0004_remove_user_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.SmallIntegerField(choices=[(0, '女'), (1, '男')], default=1, verbose_name='性别'),
        ),
        migrations.AddField(
            model_name='user',
            name='integral',
            field=models.IntegerField(default=0, verbose_name='积分'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default=15935678990, max_length=12, verbose_name='电话'),
            preserve_default=False,
        ),
    ]
