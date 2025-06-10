from django.db import models
from ForegroundApi.models import User


# Create your models here.
class Admin(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    phone = models.CharField(max_length=32, blank=True, null=True)
    role_choice = (
        ('0', '超管'),
        ('1', '商家'),
        ('2', '商家')
    )
    role = models.SmallIntegerField(choices=role_choice)


# 公告管理
class Notice(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    imgURL = models.URLField(max_length=300, blank=True, null=True,
                             default='https://tse4-mm.cn.bing.net/th/id/OIP-C.6LnWeT1-ui_FebxuImadCwHaFj?w=226&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7')


# 菜品管理

# 菜品类别，炒菜，面食，酒水等
class DishType(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# 菜品口味 ：麻辣 五香 酸辣 香辣
class DishFlavor(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# 菜品 名称 价格 描述 图片 被点次数 菜品类别 口味
class Dish(models.Model):
    dish_name = models.CharField(max_length=100)
    dish_price = models.DecimalField(max_digits=6, decimal_places=2)
    dish_desc = models.TextField()
    dish_img = models.URLField(max_length=300)
    order_count = models.IntegerField(default=0)
    # dish_flavor = models.ForeignKey(DishFlavor, on_delete=models.SET(1))
    dish_type = models.ForeignKey(DishType, on_delete=models.SET(1))


# 订单表
class Order(models.Model):
    # 这里会自动带上id，比如user_id,flavor_id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 口味外键
    flavor = models.ForeignKey(DishFlavor, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, blank=True)
    total = models.IntegerField()
    STATUS_CHOICES = (
        ('unpaid', '待支付'),
        ('paid', '已支付'),
        ('accepted', '已接单'),
        ('rejected', '已拒绝'),
        ('completed', '已完成'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='unpaid'
    )


# 订单明细表
class OrderInfo(models.Model):
    # 我们写成order，会自动在数据库中生成order_id
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    # 当前菜品的数量
    count = models.IntegerField()
    # 当前菜品的单价
    price = models.IntegerField()
    # 当前菜品的总价
    dish_total_price = models.FloatField()
