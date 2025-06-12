from django.urls import path
from .views import Login, index, Register, FindPwd, returnCode,getFlavor,GuessLike
from .views import getNotice, getDish, getRecommend, OrderView, Type,Recommend,hotDish, AddressView

urlpatterns = [
    # 登录
    path('login', Login.as_view()),
    # 注册
    path('register', Register.as_view()),
    # 找回密码
    path('findpwd', FindPwd.as_view()),
    path('', index.as_view()),
    # 获取验证码
    path('getcode', returnCode.as_view()),
    # 获取公告
    path('notice', getNotice.as_view()),
    # 获取菜品
    path('dish', getDish.as_view()),
    # 边点边推荐
    path('smartOrder',Recommend.as_view()),
    # 热门菜品
    path('hotDish',hotDish.as_view()),
    # 推荐菜品,这里是猜你喜欢
    path('guessLike', GuessLike.as_view()),
    # 获取订单
    path('order', OrderView.as_view()),
    # 获取菜品分类，比如炒菜，面食，酒水等
    path('type', Type.as_view()),
    # 获取口味
    path('flavor',getFlavor.as_view()),
    # 地址管理
    path('address', AddressView.as_view()),
]
