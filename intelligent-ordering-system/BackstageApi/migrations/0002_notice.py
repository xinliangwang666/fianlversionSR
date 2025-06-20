# Generated by Django 4.2 on 2023-04-15 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackstageApi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('notice_url', models.URLField()),
            ],
        ),
    ]
