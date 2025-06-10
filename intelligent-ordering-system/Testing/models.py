from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(verbose_name='姓名', max_length=64)
    password = models.CharField(verbose_name='密码', max_length=36)
    gender_choice = (
        (0, '女'),
        (1, '男')
    )
    gender = models.SmallIntegerField(verbose_name='性别',default=1, choices=gender_choice)
    phone = models.CharField(verbose_name='电话', max_length=12)
    integral = models.IntegerField(verbose_name='积分')


# class Dish(models.Model):
#     price = models.FloatField()
class ImgSave(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    imgURL = models.ImageField(upload_to='notices')