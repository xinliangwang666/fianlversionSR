# Generated by Django 4.2 on 2023-04-17 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackstageApi', '0014_dishflavor_desc_dishtype_desc_alter_dish_dish_flavor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='dish_flavor',
            field=models.ForeignKey(on_delete=models.SET(1), to='BackstageApi.dishflavor'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='dish_type',
            field=models.ForeignKey(on_delete=models.SET(1), to='BackstageApi.dishtype'),
        ),
    ]
