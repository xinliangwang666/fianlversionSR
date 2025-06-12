from django.db import models


# Create your models here.


class User(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=64)
    password = models.CharField(verbose_name='密码', max_length=36)
    avatar_url = models.URLField(verbose_name='用户头像', default='http://127.0.0.1:8000/media/users/avatar.jpg')
    gender_choice = (
        (0, '女'),
        (1, '男')
    )
    email = models.EmailField(default='123test@qq.com')
    gender = models.SmallIntegerField(verbose_name='性别', default=1, choices=gender_choice)
    phone = models.CharField(verbose_name='电话', max_length=12)
    integral = models.IntegerField(verbose_name='积分', default=0)
    addr = models.CharField(verbose_name='收货地址', max_length=256, null=True, blank=True)
