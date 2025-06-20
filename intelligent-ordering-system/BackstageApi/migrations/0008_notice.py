# Generated by Django 4.2 on 2023-04-16 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackstageApi', '0007_delete_notice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('imgURL', models.ImageField(upload_to='notices')),
            ],
        ),
    ]
