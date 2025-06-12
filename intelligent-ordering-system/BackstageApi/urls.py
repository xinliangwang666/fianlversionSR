
from django.urls import path
from .views import Login, AdminInfo, UserInfo, NoticeInfo, DishInfo,NewOrder
from .views import DishTypeInfo, DishFlavorInfo,OrderManage,UpdateDish
urlpatterns = [
    path('login', Login.as_view()),
    path('adminInfo', AdminInfo.as_view()),
    path('user', UserInfo.as_view()),
    # 公告管理
    path('notice', NoticeInfo.as_view()),
    #   菜品相关的接口
    path('type', DishTypeInfo.as_view()),
    # 口味管理
    path('flavor', DishFlavorInfo.as_view()),
    # 菜品管理
    path('dish', DishInfo.as_view()),
    # 修改菜品
    path('upDish',UpdateDish.as_view()),
    # 订单管理
    path('order',OrderManage.as_view()),
    # 判断是否有新订单
    path('hasNew',NewOrder.as_view()),
    path('order/update', OrderManage.as_view()),  # 订单状态更新
    path('admin/order', OrderManage.as_view(), name='order-manage'),
]
