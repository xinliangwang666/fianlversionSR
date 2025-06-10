# -*- coding: utf-8 -*-
# @Time    : 2025/5/10 21:36
# @Author  : 清风徐来
# @FileName: urls.py
# @Software: PyCharm

from django.urls import path
from .views import Login, index, Register, FindPwd, SaveImg

urlpatterns = [
    path('login', Login.as_view()),
    path('register', Register.as_view()),
    path('findpwd', FindPwd.as_view()),
    path('upload', SaveImg.as_view()),
    path('', index.as_view())
]




