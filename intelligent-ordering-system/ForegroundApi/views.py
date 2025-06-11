import json
import pprint
import pandas as pd
from scipy.spatial.distance import cosine
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.sessions.models import Session
from .models import User
from django.db import models
from django.core.mail import send_mail
import random
from django.utils import timezone
from datetime import datetime, timedelta
from BackstageApi.models import Notice, Dish, DishType, Order, OrderInfo, DishFlavor
from django.utils.decorators import method_decorator

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# 基于关联规则的推荐
from itertools import chain, combinations
from collections import defaultdict
import numpy as np
from django.db.models import Count


# 自定义装饰器，用于判断用户的身份
def check_session_id(func):
    def wrapper(request, *args, **kwargs):
        try:
            print(request.headers.get('Authorization'))
            session_id = request.headers.get('Authorization', False).split(' ')[1]
        except (AttributeError, IndexError):
            return JsonResponse({'status': 'error', 'msg': '非法访问'}, status=401)
        if session_id is not None:
            try:
                session = Session.objects.get(session_key=session_id)

            except Session.DoesNotExist:
                session = None
                # 如果通过当前sessionid可以获取到数据
            if session is not None:
                user_data = session.get_decoded()
                print('当前登录用户', user_data['info'])
                return func(request, *args, **kwargs)
            else:
                return JsonResponse({'status': 'error', 'msg': "非法访问"}, status=401)
        else:
            return JsonResponse({'status': 'error'}, status=401)

    return wrapper


# 登录逻辑
class Login(View):
    def post(self, request):
        data = json.loads(request.body)
        name = data.get('username')
        password = data.get('password')
        print(name, password)

        if name and password:
            res = User.objects.filter(name=name, password=password)
            if res.exists():
                userInfo = res.first()
                obj = {
                    'id': userInfo.id,
                    'name': name,
                    'password': password,
                    'integral': userInfo.integral,
                    'avatar_url': userInfo.avatar_url
                }

                # userid = userInfo.id
                # avatar_url = res.first().avatar_url
                # obj['id'] = userid
                request.session.save()
                request.session['info'] = obj
                # 设置过期时间，设置一周内过期
                expires = datetime.now() + timedelta(days=7)
                request.session.set_expiry(expires)
                session_id = request.session.session_key
                print(session_id)
                response = JsonResponse(
                    {"avatar_url": userInfo.avatar_url, "integral": userInfo.integral, 'sessionid': session_id},
                    status=200)
                return response

            else:
                return JsonResponse({'status': 'error', 'msg': '账号或密码错误'}, status=401)
        else:
            return HttpResponseBadRequest('请检查相关字段')


# 注册逻辑
class Register(View):

    def post(self, request):
        data = json.loads(request.body)
        name = data.get('name')
        password = data.get('password')
        phone = data.get('phone')
        email = data.get('email')
        gender = data.get('gender', 1)
        integral = 0
        print(name, password, phone, gender, integral, email)
        
        # 先检查必填字段是否都存在
        if not all([name, password, phone, email]):
            return JsonResponse({'status': 'error', 'msg': '缺少必填字段'}, status=400)
            
        # 分别检查用户名和手机号是否已被注册
        if User.objects.filter(name=name).exists():
            return JsonResponse({'status': 'error', 'msg': '该用户名已被注册'}, status=400)
            
        if User.objects.filter(phone=phone).exists():
            return JsonResponse({'status': 'error', 'msg': '该手机号已被注册'}, status=400)
            
        # 如果都没有重复，创建新用户
        obj = {'name': name, 'password': password, 'phone': phone, 'gender': gender, 'integral': integral}
        if gender == '0':
            obj['avatar_url'] = 'http://127.0.0.1:8000/media/users/girl.jpg'
        else:
            obj['avatar_url'] = 'http://127.0.0.1:8000/media/users/boy.jpg'
        print(obj)
        user = User(**obj)
        user.save()
        return JsonResponse({'status': 'success', 'data': obj})


# 发送新密码以及验证码
class FindPwd(View):

    # 获取验证码
    # @method_decorator(check_session_id)

    # 提交验证码，必须携带codeid
    def post(self, request):

        try:
            print(request.headers.get('Authorization'))
            code_id = request.headers.get('Authorization').split(' ')[1]
        except (AttributeError, IndexError):
            return JsonResponse({'status': 'error', 'msg': '非法访问'}, status=401)
        if code_id is not None:
            try:
                session = Session.objects.get(session_key=code_id)

            except Session.DoesNotExist:
                session = None
                # 如果通过当前sessionid可以获取到数据
            if session is not None:
                code_data = session.get_decoded()
                code = code_data['code']['code']
            else:
                return JsonResponse({'status': 'error', 'msg': '验证码已失效'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'msg': '验证码已失效'}, status=400)

        print('验证码存在并且没有过期')
        # 之前是验证身份，如果有code_id，并且没有过期才会走下面的逻辑
        data = json.loads(request.body)
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        post_code = data.get('code')
        pwd = data.get('pwd')
        newpwd = data.get('newpwd')
        print(f'当前接收到的数据为--name:{name},phone:{phone},email:{email},post_code:{post_code},pwd:{pwd},newpwd:{newpwd}')

        if code == post_code:
            res = User.objects.filter(name=name, phone=phone).update(password=newpwd)
            if res > 0:
                return JsonResponse({'status': 'success'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'msg': '修改失败'}, status=400)

        else:
            return JsonResponse({'status': 'error', 'msg': '验证码错误'}, status=400)


# 获取验证码
class returnCode(View):

    def _get_code(self, length=6):
        # 随机选择字符集合
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        # 生成随机字符串
        code = ''.join(random.choice(chars) for i in range(length))
        return code

    def get(self, request):
        email = request.GET.get('email')
        code = self._get_code()
        res = send_mail("飞飞点餐", f"您的验证码是:{code},验证码五分钟内有效", "zx529213@qq.com", [email])
        # res大于0则说明发送成功
        print(f'email:{email},code:{code}')
        if res > 0:
            request.session.save()
            request.session['code'] = {'code': code}
            # 设置过期时间，验证码五分钟内有效
            expires = datetime.now() + timedelta(minutes=5)
            request.session.set_expiry(expires)
            codeid = request.session.session_key
            print(codeid)
            response = JsonResponse({'status': 'success', 'codeid': codeid, 'msg': '验证码已发送，五分钟内有效'}, status=200)
            return response
        else:
            return JsonResponse({'status': 'error', 'msg': '验证码发送失败'}, status=400)
    # def post(self,request):
    #     pass


class index(View):
    def get(self, request):
        queryn = request.GET.get('name')
        print(queryn)
        # return HttpResponse('欢迎光临，这是index页面')
        return JsonResponse({"data": {"name": "zs"}}, status=200)

    def post(self, request):
        codeid = request.headers.get('Authorization').split(' ')[1]
        print('当前的codeid', codeid)
        try:
            session = Session.objects.get(session_key=codeid, expire_date__gte=timezone.now())
            print('获取到了session', session)
        except Session.DoesNotExist:
            session = None
        # 如果通过当前sessionid可以获取到数据

        if session is not None:
            user_code = session.get_decoded()

            print('当前登录用户', user_code['code'])
            code = user_code['code']['code']

            data = json.loads(request.body)
            name = data.get('name', None)
            age = data.get('age', 1000)
            codes = data.get('code', '8848')
            print(f'code:{code},codes:{codes}', code == codes)
            if code == codes:
                return JsonResponse({"status": "success", "msg": "登陆成功"})
            print(f'当前codeid：{codeid},获取到的对应验证码为{code}')
            print(name, age)
            return JsonResponse({"status": "error", "msg": "验证码错误"}, status=400)
        else:
            print('codeid过期或已经失效')
            return JsonResponse({"status": "验证码已失效"}, status=400)


# 轮播图-公告列表
class getNotice(View):
    # @method_decorator(check_session_id)
    def get(self, request):
        notice_list = []
        notices = Notice.objects.all()
        count = notices.count()
        # 因为前端使用的第三方轮播图，只有image和titie属性
        for notice in notices:
            obj = {
                'id': notice.id,
                'titles': notice.title,
                'title': notice.description,
                'pub_date': notice.pub_date,
                'image': notice.imgURL
            }
            notice_list.append(obj)
        return JsonResponse({
            "noticeList": notice_list,
            "count": count
        })


# 获取菜品列表
class getDish(View):
    # @method_decorator(check_session_id)
    def get(self, request):
        dish_list = []
        dishes = Dish.objects.all()
        count = dishes.count()
        for dish in dishes:
            obj = {
                'id': dish.id,
                'name': dish.dish_name,
                'price': dish.dish_price,
                'desc': dish.dish_desc,
                'dish_img': dish.dish_img,
                'dish_type': dish.dish_type.name,
                'order_count': dish.order_count
            }
            dish_list.append(obj)
        return JsonResponse({
            "dishList": dish_list,
            "count": count
        })


# 推荐页面
class getRecommend(View):
    # 如果用户没有登录或者没有点餐记录，就按照销量推荐
    # 如果用户有点餐记录，则按照内容进行推荐
    def get(self, request):
        dish_list = []
        dishes = Dish.objects.all().order_by('-order_count')[:20]
        count = dishes.count()
        for dish in dishes:
            obj = {
                'id': dish.id,
                'name': dish.dish_name,
                'price': dish.dish_price,
                'desc': dish.dish_desc,
                'dish_img': dish.dish_img,
                'order_count': dish.order_count
            }
            dish_list.append(obj)
        return JsonResponse({
            "dishList": dish_list,
            "count": count
        })


# 热门菜品
class hotDish(View):
    def get(self, request):
        dish_list = []
        dishes = Dish.objects.all().order_by('-order_count')[:10]
        count = dishes.count()
        for dish in dishes:
            obj = {
                'id': dish.id,
                'name': dish.dish_name,
                'price': dish.dish_price,
                'desc': dish.dish_desc,
                'dish_img': dish.dish_img,
                'order_count': dish.order_count
            }
            dish_list.append(obj)
        return JsonResponse({
            "dishList": dish_list,
            "count": count
        })


# 猜你喜欢
class GuessLike(View):
    @method_decorator(check_session_id)
    def get(self, request):
        session_id = request.headers.get('Authorization').split(' ')[1]
        session = Session.objects.get(session_key=session_id)
        user_data = session.get_decoded()

        user_id = user_data['info']['id']
        # 订单表中查找到该用户的所有订单
        dish_count_dict = defaultdict(int)
        orders = Order.objects.filter(user_id=user_id)
        if orders.exists():
            # 遍历所有订单，在订单详情表中查询到它的点菜记录
            for order in orders:
                dishes = OrderInfo.objects.filter(order=order)
                for di in dishes:
                    dish_count_dict[di.dish_id] += 1

            # 对菜品按出现次数进行排序
            sorted_dish_list = sorted(
                dish_count_dict.items(),
                key=lambda x: x[1],
                reverse=True
            )

            # 将排好序的菜品信息组装成字典
            dish_list = []
            for dish_id, count in sorted_dish_list:
                dish = Dish.objects.get(id=dish_id)
                dish_info = {
                    "id": dish.id,
                    "price": dish.dish_price,
                    "desc": dish.dish_desc,
                    "name": dish.dish_name,
                    "img": dish.dish_img,
                    "count": count
                }
                dish_list.append(dish_info)

            return JsonResponse({
                "dishList": dish_list,
                "total": len(dish_list)
            })
        else:
            return JsonResponse({
                "dishList": [],
                "total": 0
            })

    # def get(self, request):
    #     session_id = request.headers.get('Authorization').split(' ')[1]
    #     session = Session.objects.get(session_key=session_id)
    #     user_data = session.get_decoded()
    #
    #     user_id = user_data['info']['id']
    #     # 订单表中查找到该用户的所有订单
    #     dish_list = []
    #     orders = Order.objects.filter(user_id=user_id)
    #     if orders.exists():
    #         # order_list = []
    #         # 遍历所有订单，在订单详情表中查询到它的点菜记录
    #         for order in orders:
    #             dishes = OrderInfo.objects.filter(order=order)
    #             print(dishes.values())
    #             for di in dishes:
    #                 dish_info = {
    #                     "id": di.dish_id,
    #                     "price": di.dish.dish_price,
    #                     "desc": di.dish.dish_desc,
    #                     "name": di.dish.dish_name,
    #                     "img": di.dish.dish_img
    #                 }
    #                 dish_list.append(dish_info)
    #
    #         return JsonResponse({
    #             "dishList": dish_list,
    #             "total": len(dish_list)
    #         })
    #     else:
    #         return JsonResponse({
    #             "dishList": [],
    #             "total": 0
    #         })


# 订单页面
class OrderView(View):
    @method_decorator(check_session_id)
    def get(self, request):
        session_id = request.headers.get('Authorization').split(' ')[1]
        session = Session.objects.get(session_key=session_id)
        user_data = session.get_decoded()

        user_id = user_data['info']['id']
        orders = Order.objects.filter(user_id=user_id)
        if orders.exists():
            order_list = []
            for order in orders:
                order_info = {
                    "order_id": order.id,
                    "order_time": order.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "order_total": order.total,
                    "order_flavor": order.flavor.name,  # 假设DishFlavor有name字段
                    "order_status": order.get_status_display(),  # 使用中文状态
                    "dishes": []
                }
                order_num = 0
                dish_infos = OrderInfo.objects.filter(order=order)
                for di in dish_infos:
                    # 关键修复：直接使用dish_img字段值（假设为字符串URL）
                    dish_img = di.dish.dish_img if di.dish.dish_img else ""
                    dish_info = {
                        "id": di.dish.id,
                        "dish_price": di.price,
                        "dish_count": di.count,
                        "dish_total_price": di.dish_total_price,
                        "dish_name": di.dish.dish_name,
                        "dish_img": dish_img  # 移除.url
                    }
                    order_num += di.count
                    order_info["dishes"].append(dish_info)
                order_info["order_num"] = order_num
                order_list.insert(0, order_info)

            total = len(order_list)
            return JsonResponse({
                "order_list": order_list,
                "total": total
            })
        else:
            return JsonResponse({
                "status": "success",
                "data": {
                    "order_list": [],
                    "total": 0
                }
            })

    @method_decorator(check_session_id)
    def post(self, request):
        data = json.loads(request.body)
        session_id = request.headers.get('Authorization').split(' ')[1]
        session = Session.objects.get(session_key=session_id)
        user_data = session.get_decoded()
        user_id = user_data['info']['id']
        flavor_id = data.get('flavor_id', 1)  # 设置默认口味
        total = data.get('total')
        dishes = data.get('dishes', [])
        is_paid = data.get('is_paid', False)

        # 确定订单状态
        order_status = 'paid' if is_paid else 'unpaid'

        try:
            order = Order.objects.create(
                flavor_id=flavor_id,
                user=User.objects.get(id=user_id),
                total=total,
                status=order_status
            )

            for dish in dishes:
                dish_obj = Dish.objects.get(id=dish["id"])
                OrderInfo.objects.create(
                    dish=dish_obj,
                    order=order,
                    count=dish["num"],
                    price=dish_obj.dish_price,
                    dish_total_price=dish["num"] * dish_obj.dish_price
                )
                # 更新菜品销量
                dish_obj.order_count = models.F('order_count') + dish["num"]
                dish_obj.save()
            if is_paid:
                user = User.objects.get(id=user_id)
                points_to_add = int(total / 10)  # 支付金额/10作为积分
                user.integral += points_to_add
                user.save()
            return JsonResponse({
                "status": "success",
                "msg": "订单创建成功",
                "order_id": order.id,
                "order_status": order.get_status_display()
            })
        except Exception as e:
            return JsonResponse({"status": "error", "msg": str(e)}, status=400)

# 添加支付回调接口
class PaymentCallback(View):
    def post(self, request):
        data = json.loads(request.body)
        order_id = data.get('order_id')
        payment_success = data.get('success', False)

        try:
            order = Order.objects.get(id=order_id)

            if payment_success and order.status == 'unpaid':
                order.status = 'paid'
                order.save()
                return JsonResponse({"status": "success", "msg": "支付成功"})
            else:
                return JsonResponse({"status": "error", "msg": "支付失败"}, status=400)
        except Order.DoesNotExist:
            return JsonResponse({"status": "error", "msg": "订单不存在"}, status=404)


# 菜品分类
class Type(View):
    def get(self, request):
        type_list = []
        all_type = DishType.objects.all()
        for dish_type in all_type:
            obj = {
                "id": dish_type.id,
                "name": dish_type.name,
                "desc": dish_type.desc
            }
            type_list.append(obj)
        count = all_type.count()
        return JsonResponse({"typeList": type_list, "total": count})


# 基于用户偏好的推荐
class Recommend2(View):
    def __init__(self):
        # 获取所有菜品的id和描述信息
        dishes = Dish.objects.values('id', 'dish_desc', 'dish_type__name')

        # 将所有菜品的描述信息和类型信息进行字符串拼接
        combined_descriptions = []
        for di in dishes:
            clean_desc = di['dish_desc'].replace('\n', ' ').replace('\r', '')
            typename = di['dish_type__name']
            combined = clean_desc + typename
            combined_descriptions.append(combined)

        # 初始化TfidfVectorizer对象，并将所有菜品的描述信息及类型信息转换为TF-IDF矩阵
        self.tfidf = TfidfVectorizer()
        self.tfidf_matrix = self.tfidf.fit_transform(combined_descriptions)

        # 将菜品的ID与在TF-IDF矩阵中的索引之间建立映射关系
        self.dish_id_to_index = {}
        for index, dish in enumerate(dishes):
            self.dish_id_to_index[dish['id']] = index

    # 用户校验，如果没有登录则不进行推荐
    @method_decorator(check_session_id)
    def post(self, request):
        # 获取购物车内的菜品
        data = json.loads(request.body)
        cart = data.get('cartId')
        print('当前的购物车内的菜品id', cart)

        # 判断用户是否有订单记录，如果没有则使用物品相似度进行推荐
        session_id = request.headers.get('Authorization').split(' ')[1]
        session = Session.objects.get(session_key=session_id)
        user_data = session.get_decoded()
        user_id = user_data['info']['id']
        orders = Order.objects.filter(user_id=user_id)
        # 如果没有历史订单记录
        if not orders.exists():
            # print('当前是新用户，没有订单记录')
            recommendations = self.recommendations2(cart)
            return JsonResponse({"data": list(recommendations)})

        # 如果订单记录数小于20，则使用协同过滤进行推荐
        order_count = orders.count()
        print('当前用户订单数', order_count)
        if order_count < 20:
            # print('当前用户有过点餐记录')
            # recommendations = self.get_cart_similarity(cart, user_id)
            recommendations = self.recommends(cart, user_id)
            # 创建推荐器对象，并使用用户历史订单数据来训练
        #     recommender = Recommender()
        #     recommender.fit(user_id)
        # #     使用购物车信息进行推荐，返回结果
        #     recommendations = recommender.predict(cart)

        # 否则使用历史订单进行推荐
        else:
            print('当前用户有超过20条订单记录')
            recommendations = self.get_history_similarity(user_id, cart)

        return JsonResponse({"data": list(recommendations)})

    def get_recommendations(self, cart):
        print('当前是新用户，没有点餐记录')
        print('cart', cart)
        # 获取所有菜品的id和描述信息
        dishes = Dish.objects.values('id', 'dish_desc', 'dish_type__name')

        # 记录菜品的id和索引之间的对应关系
        dish_id_to_index = {}
        for index, dish in enumerate(dishes):
            dish_id_to_index[dish['id']] = index
        # 获取所有菜品的描述信息
        # descriptions = [dish['dish_desc'] for dish in dishes]
        descriptions = []
        for di in dishes:
            clean_desc = di['dish_desc'].replace('\n', ' ').replace('\r', '')
            typename = di['dish_type__name']
            # print(clean_desc)
            descriptions.append(clean_desc + typename)
        # print(descriptions[3])
        # 初始化TfidfVectorizer，将所有菜品的描述信息转换为TF-IDF向量
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(descriptions)

        # 根据购物车内的菜品，获取相应的属性信息
        selected_dishes = Dish.objects.filter(id__in=cart).values_list('dish_desc', 'dish_type__name')

        # 将所有菜品的描述信息和类型信息进行字符串拼接
        combined_descriptions = []
        for di in dishes:
            clean_desc = di['dish_desc'].replace('\n', ' ').replace('\r', '')
            typename = di['dish_type__name']
            combined = clean_desc + typename
            # print(combined)
            combined_descriptions.append(combined)

        # 将购物车内菜品的描述信息和类型信息进行字符串拼接
        selected_combined_descriptions = [d[0].replace('\n', ' ').replace('\r', '') + d[1] for d in selected_dishes]

        # 计算购物车内菜品的TF-IDF向量
        cart_tfidf = tfidf.transform(selected_combined_descriptions)

        # 计算购物车内菜品与其他菜品之间的余弦相似度
        sim_scores = cosine_similarity(cart_tfidf, tfidf_matrix)

        # 获取与购物车内菜品相似度最高的前n个菜品的索引
        n = 10
        sim_scores = sim_scores[0]
        similar_dish_indices = sim_scores.argsort()[:-n - 1:-1]

        # 将菜品的索引转换为菜品的id
        similar_dish_ids = [dishes[int(index)]['id'] for index in similar_dish_indices]

        # 查询数据库获取推荐菜品的详细信息
        similar_dishes = Dish.objects.filter(id__in=similar_dish_ids)

        # 过滤购物车内已经包含的菜品
        similar_dishes = similar_dishes.exclude(id__in=cart)
        print('推荐的菜品结果id', similar_dish_ids)
        # 返回推荐结果
        return similar_dishes.values()

    # 购物车内的菜品进行计算
    def get_cart_similarity(self, cart, user_id):
        # 获取用户购买过的所有订单的订单号
        orders = Order.objects.filter(user_id=user_id).values_list('id', flat=True)

        # 获取所有订单中的菜品ID
        dish_ids = OrderInfo.objects.filter(order_id__in=orders).values_list('dish_id', flat=True)

        # 获取所有菜品的属性信息
        purchased_dishes = Dish.objects.filter(id__in=dish_ids).values_list('dish_desc', flat=True)

        # 初始化TfidfVectorizer，将所有菜品的描述信息转换为TF-IDF向量
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(purchased_dishes)

        # 根据购物车内的菜品，获取相应的属性信息
        selected_dishes = Dish.objects.filter(id__in=cart).values_list('dish_desc', flat=True)

        # 计算购物车内菜品的TF-IDF向量
        cart_tfidf = tfidf.transform(selected_dishes)

        # 计算购物车内菜品和用户购买过的所有菜品之间的余弦相似度
        sim_scores = cosine_similarity(cart_tfidf, tfidf_matrix)

        # 获取与购物车内菜品相似度最高的前n个菜品
        n = 10
        sim_scores = sim_scores[0]
        similar_dish_indices = sim_scores.argsort()[:-n:-1]

        # 获取相似度最高的菜品的id
        similar_dish_ids = [dish_ids[int(i)] for i in similar_dish_indices]

        # 查询数据库获取推荐菜品的详细信息
        similar_dishes = Dish.objects.filter(id__in=similar_dish_ids)

        # 过滤购物车内已经包含的菜品
        similar_dishes = similar_dishes.exclude(id__in=cart)

        # 返回推荐结果
        return similar_dishes.values()

    def recommendations2(self, cart):
        print('当前是新用户，没有点餐记录')
        print('cart', cart)

        # 根据购物车中的菜品获取它们的描述信息和类型信息，并将它们进行字符串拼接以得到购物车的TF-IDF向量
        selected_dishes = Dish.objects.filter(id__in=cart).values_list('dish_desc', 'dish_type__name')
        selected_combined_descriptions = [d[0].replace('\n', ' ').replace('\r', '') + d[1] for d in selected_dishes]
        cart_tfidf = self.tfidf.transform(selected_combined_descriptions)

        # 计算购物车中菜品与所有菜品的相似度
        sim_scores = cosine_similarity(cart_tfidf, self.tfidf_matrix)

        # 获取与购物车内菜品相似度最高的前n个菜品的索引
        n = 10
        sim_scores = sim_scores[0]
        similar_dish_indices = sim_scores.argsort()[:-n - 1:-1]

        # 将菜品的索引转换为菜品的id
        similar_dish_ids = [list(self.dish_id_to_index.keys())[list(self.dish_id_to_index.values()).index(int(index))]
                            for index in similar_dish_indices]

        # 查询数据库获取推荐菜品的详细信息
        similar_dishes = Dish.objects.filter(id__in=similar_dish_ids)

        # 过滤购物车内已经包含的菜品
        similar_dishes = similar_dishes.exclude(id__in=cart)
        print('推荐的菜品结果id', similar_dish_ids)

        # 返回推荐结果
        return similar_dishes.values()

    # 基于用户偏好的推荐
    def recommends(self, cart, user_id):
        # 查询用户购买过的所有菜品
        user_purchased = OrderInfo.objects.filter(order__user_id=user_id).values('dish_id')

        # 获取购物车中未在用户购买记录中出现过的菜品
        new_items = Dish.objects.filter(id__in=cart).exclude(id__in=user_purchased)

        # 查询所有菜品的属性信息
        all_items = Dish.objects.all().select_related('dishflavor', 'dishtype').annotate(
            flavor_name=Count('dishflavor__name', distinct=True),
            dish_type_name=Count('dishtype__name', distinct=True),
        )

        # 构建用户-菜品偏好矩阵
        pref_matrix = []

        for item in all_items:
            pref = 0

            # 如果菜品在用户购买记录中出现过，赋予高权重（例如1）
            if item.id in user_purchased.values_list('dish_id', flat=True):
                pref += 1

            # 如果菜品在购物车中出现过，赋予较高权重（例如0.5）
            if item.id in cart:
                pref += 0.5

            # 如果菜品的口味与用户口味相近，赋予较高权重（例如0.3）
            if item.flavor_name > 0:
                user_flavors = User.objects.get(id=user_id).fav_flavor.all().values_list('name', flat=True)
                for flavor in item.flavor.all():
                    if flavor.name in user_flavors:
                        pref += 0.3

            # 如果菜品类别与用户口味相近，赋予较高权重（例如0.2）
            if item.dish_type_name > 0:
                user_types = User.objects.get(id=user_id).fav_dish_type.all().values_list('name', flat=True)
                for dish_type in item.dish_type.all():
                    if dish_type.name in user_types:
                        pref += 0.2

            pref_matrix.append((item.id, pref))

        # 将偏好矩阵转换为DataFrame格式并计算相似度
        df = pd.DataFrame(pref_matrix, columns=['id', 'rating']).set_index('id')
        item_sim = pd.DataFrame(index=df.index, columns=df.index)

        for i in range(len(item_sim.columns)):
            for j in range(len(item_sim.columns)):
                item_sim.iloc[i, j] = 1 - cosine(df.iloc[:, i], df.iloc[:, j])

        # 获取购物车中菜品的相似菜品并根据相似度进行排序
        sim_items = pd.DataFrame()

        for item in cart:
            sim_items = sim_items.append(
                item_sim[item].drop(item).sort_values(ascending=False).to_frame().reset_index())

        sim_items.columns = ['id', 'similarity']

        # 按照相似度降序排列并且选取关联度比较高的菜品
        sim_items = sim_items.sort_values(by='similarity', ascending=False).head()

        # 获取关联度比较高的菜品的具体信息
        rec_items = Dish.objects.filter(id__in=sim_items['id']).select_related('flavor', 'dish_type')

        return rec_items.values()

    def get_history_similarity(self, user_id, cart):
        # print('当前是老用户，订单数大于20')

        # 获取用户购买过的所有订单的订单号
        orders = Order.objects.filter(user_id=user_id).values_list('id', flat=True)

        # 获取所有订单中的菜品ID
        dish_ids = OrderInfo.objects.filter(order_id__in=orders).values_list('dish_id', flat=True)

        # 获取所有菜品的属性信息
        purchased_dishes = Dish.objects.filter(id__in=dish_ids).values_list('dish_desc', flat=True)

        # 初始化TfidfVectorizer，将所有菜品的描述信息转换为TF-IDF向量
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(purchased_dishes)
        # 获取购物车内的菜品ID，并筛选出对应的历史订单中的菜品ID
        cart_dish_ids = cart
        filtered_dish_indices = []
        for i, dish_id in enumerate(dish_ids):
            if dish_id not in cart_dish_ids:
                filtered_dish_indices.append(i)

        # 计算用户历史订单中除购物车内菜品外的所有菜品之间的余弦相似度
        sim_scores = cosine_similarity(tfidf_matrix[filtered_dish_indices])

        # 获取相似度最高的前n个菜品
        n = 10
        similar_dish_indices = sim_scores.argsort()[:-n - 1:-1]
        similar_dish_indices = [filtered_dish_indices[i] for i in similar_dish_indices]

        # 获取相似度最高的菜品的id
        similar_dish_ids = [dish_ids[int(i)] for i in similar_dish_indices]

        # 查询数据库获取推荐菜品的详细信息
        similar_dishes = Dish.objects.filter(id__in=similar_dish_ids)

        # 返回推荐结果
        return similar_dishes.values()


# 基于关联规则的推荐算法
class Recommender:
    def __init__(self, min_support=0.1, min_confidence=0.7, max_items=20):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.max_items = max_items
        self.frequent_itemsets = None
        self.support_data = None

    def powerset(self, iterable):
        """生成一个可迭代的幂集"""
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

    def generate_rules(self, frequent_itemsets, support_data, min_confidence):
        """根据频繁项集和支持度信息，生成关联规则"""
        rules = []
        for itemset in frequent_itemsets:
            if len(itemset) > 1:
                for item in itemset:
                    antecedent = itemset - frozenset([item])
                    consequent = frozenset([item])
                    confidence = support_data[itemset] / support_data[antecedent]
                    if confidence >= min_confidence:
                        rules.append((antecedent, consequent, confidence))
        return rules

    def fit(self, user_id):
        # 获取用户购买过的所有订单的订单号
        orders = Order.objects.filter(user_id=user_id).values_list('id', flat=True)
        # 获取所有订单中的菜品ID
        dish_ids = OrderInfo.objects.filter(order_id__in=orders).values_list('dish_id', flat=True)

        # 统计每个菜品的出现次数
        item_counts = {}
        for dish_id in dish_ids:
            # 判断该菜品是否在item_counts中出现过，若出现过则将其count值加1，否则新建一条记录
            if dish_id in item_counts:
                item_counts[dish_id] += 1
            else:
                item_counts[dish_id] = 1
        print(item_counts)
        # 计算支持度，去除不满足支持度阈值的菜品
        num_orders = len(orders)
        support_data = {}
        itemsets = set()
        for item, count in item_counts.items():
            support = count / num_orders
            if support >= self.min_support:
                itemsets.add(frozenset([item]))
                support_data[frozenset([item])] = support

        # 迭代生成更大的菜品子集，直到不能再合并为止
        k = 2
        while len(itemsets) > 0:
            # 构造k项候选集
            candidate_itemsets = set()
            for i, itemset1 in enumerate(itemsets):
                for itemset2 in list(itemsets)[i + 1:]:
                    new_itemset = itemset1 | itemset2
                    if len(new_itemset) == k:
                        candidate_itemsets.add(new_itemset)

            # 统计候选集中每个菜品子集的出现次数
            item_counts = defaultdict(int)
            for order_id in orders:
                order_dish_ids = set(OrderInfo.objects.filter(order_id=order_id).values_list('dish_id', flat=True))
                for itemset in candidate_itemsets:
                    if itemset.issubset(order_dish_ids):
                        item_counts[itemset] += 1

            # 计算支持度，去除不满足支持度阈值的菜品
            itemsets = set()
            for itemset, count in item_counts.items():
                support = count / num_orders
                if support >= self.min_support:
                    itemsets.add(itemset)
                    support_data[itemset] = support

            k += 1

        # 生成关联规则
        self.frequent_itemsets = [itemset for itemset in itemsets if len(itemset) > 1]
        self.support_data = support_data
        self.rules = self.generate_rules(self.frequent_itemsets, self.support_data, self.min_confidence)
        print('self.frequent_itemsets', self.frequent_itemsets)

    def predict(self, cart):
        # 根据购物车的菜品，找到相关的所有备选菜品
        items = set(cart)
        # print(items)
        itemsets = []
        for itemset in self.frequent_itemsets:
            if len(itemset & items) > 0:
                itemsets.append(itemset)
        print('items', items)
        print('itemsets', itemsets)
        # 计算备选菜品的得分，并按照得分排序
        scores = defaultdict(float)
        for itemset in itemsets:
            for item in itemset - items:
                confidence = self.support_data[itemset] / self.support_data[itemset - {item}]
                score = confidence * self.support_data[itemset]
                scores[item] += score
        print('score', scores)
        recommended_items = sorted(scores, key=lambda x: -scores[x])[:self.max_items]
        recommended_dishes = Dish.objects.filter(id__in=recommended_items).exclude(id__in=cart)

        return recommended_dishes.values()


# 推荐系统 根据用户的订单数来做不同的推荐
class Recommend(View):
    # 用户校验，如果没有登录则不进行推荐
    @method_decorator(check_session_id)
    def post(self, request):
        # 获取购物车内的菜品
        data = json.loads(request.body)
        cart = data.get('cartId')
        # 判断用户是否有订单记录,当走到这里必然存在用户信息，所以不做判断
        session_id = request.headers.get('Authorization').split(' ')[1]
        session = Session.objects.get(session_key=session_id)
        user_data = session.get_decoded()
        user_id = user_data['info']['id']
        orders = Order.objects.filter(user_id=user_id)
        # 如果订单信息存在，则计算与之相似度最高的5个用户的订单信息
        if orders.exists():
            print('order存在，count为', orders.count())
            if orders.count() > 10:
                print('当前用户订单数大于10，推荐用户历史订单内的菜品')
                recommendations = self.get_recommendations_based_history(cart=cart, user_id=user_id)
            else:
                print('当前用户有点餐记录，根据用户的点餐记录计算出和它相似度高的用户所点的菜品')
                recommendations = self.get_recommendations_based_on_cart_and_user_id(cart,user_id,15)
        else:
            print('用户没有点餐记录，使用基于内容的推荐算法')

            recommendations = self.get_recommendatsion_based_cart(cart)

            # 返回推荐结果

        return JsonResponse({"data": list(recommendations)})

    # 有过点餐记录
    # def get_recommendations_based_order(self, cart, user_id):
    #     # 获取用户购买过的所有订单的订单号
    #     orders = Order.objects.filter(user_id=user_id).values_list('id', flat=True)
    #     # 获取所有订单中的菜品ID
    #     dish_ids = OrderInfo.objects.filter(order_id__in=orders).values_list('dish_id', flat=True)
    #     # 获取用户订单的的属性信息，包括菜品描述和菜品类型
    #     purchased_dishes = Dish.objects.filter(id__in=dish_ids).values_list('id', 'dish_desc', 'dish_type__name')
    #     # 将所有菜品的描述信息和类型信息进行字符串拼接，并删除换行符
    #     combined_descriptions = []
    #     for di in purchased_dishes:
    #         clean_desc = di[1].replace('\n', ' ').replace('\r', '')
    #         typename = di[2]
    #         combined = clean_desc + ' ' + typename
    #         combined_descriptions.append(combined)
    #     print('获取用户订单的菜品信息')
    #     print(combined_descriptions[0])
    #     # 初始化TfidfVectorizer，将所有菜品的描述信息与类型信息转换为TF-IDF向量
    #     tfidf = TfidfVectorizer()
    #     tfidf_matrix = tfidf.fit_transform(combined_descriptions)
    #
    #     # 获取用户的购物车内菜品信息，包括菜品ID，菜品描述和菜品类型
    #     selected_dishes = Dish.objects.filter(id__in=cart).values_list('id', 'dish_desc', 'dish_type__name')
    #
    #     # 将所有菜品的描述信息和类型信息进行字符串拼接，并删除换行符
    #     selected_combined_descriptions = []
    #     for di in selected_dishes:
    #         clean_desc = di[1].replace('\n', ' ').replace('\r', '')
    #         typename = di[2]
    #         combined = clean_desc + ' ' + typename
    #         selected_combined_descriptions.append(combined)
    #     print('购物车内的菜品信息')
    #     print(selected_combined_descriptions[0])
    #     # 计算购物车内菜品的TF-IDF向量
    #     cart_tfidf = tfidf.transform(selected_combined_descriptions)
    #
    #     # 计算购物车内菜品与用户购买过的所有菜品之间的余弦相似度
    #     sim_scores = cosine_similarity(cart_tfidf, tfidf_matrix)
    #
    #     # 获取与购物车内菜品相似度最高的前n个用户的所有订单
    #     n = 5
    #     user_sim_scores = sim_scores[0]
    #     similar_user_ids = user_sim_scores.argsort()[:-n - 1:-1] + 1  # 加一表示从 1 开始的用户 ID
    #
    #     similar_user_orders = Order.objects.filter(user_id__in=similar_user_ids).values_list('id', flat=True)
    #
    #     # 获取这些订单中的所有菜品ID
    #     similar_user_dish_ids = OrderInfo.objects.filter(order_id__in=similar_user_orders).values_list(
    #         'dish_id', flat=True)
    #
    #     # 获取这些菜品的属性信息，包括菜品描述和菜品类型
    #     similar_dishes = Dish.objects.filter(id__in=similar_user_dish_ids).values_list('id', 'dish_desc',
    #                                                                                    'dish_type__name')
    #
    #     # 计算购物车内菜品和这些菜品之间的相似度
    #     selected_dish_ids = set([d[0] for d in selected_dishes])
    #     similar_dish_indices = set(d[0] for d in similar_dishes) - selected_dish_ids
    #
    #     # 获取推荐结果
    #     recommendations = Dish.objects.filter(id__in=similar_dish_indices)
    #     return recommendations.values()
    #     # res = recommendations.values()
    #     # return random.shuffle(res)
    '''
    获取用户购买过的所有订单的订单号。
    获取所有订单中的菜品 ID，进而获取用户订单的属性信息，包括菜品描述和菜品类型。
    初始化 TfidfVectorizer，将所有菜品的描述信息与类型信息转换为 TF-IDF 向量。
    获取用户的购物车内菜品信息，包括菜品 ID，菜品描述和菜品类型。
    计算购物车内菜品与用户购买过的所有菜品之间的余弦相似度，得到一个相似度矩阵。
    获取与购物车内菜品相似度最高的前 n 个用户的所有订单。
    获取这些订单中的所有菜品 ID，进而获取这些菜品的属性信息，包括菜品描述和菜品类型。
    计算购物车内菜品和这些菜品之间的相似度。
    获取推荐结果。
'''
    def get_recommendations_based_on_cart_and_user_id(self, cart, user_id, n=2):
        # 获取所有历史订单中点过的菜品
        all_user_dish_ids = OrderInfo.objects.all().values_list('dish_id', flat=True)
        purchased_dishes = Dish.objects.filter(id__in=all_user_dish_ids).values_list('id', 'dish_desc',
                                                                                     'dish_type__name')
        combined_descriptions = []
        for di in purchased_dishes:
            clean_desc = di[1].replace('\n', ' ').replace('\r', '')
            typename = di[2]
            combined = clean_desc + ' ' + typename
            combined_descriptions.append(combined)

        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(combined_descriptions)

        selected_dishes = Dish.objects.filter(id__in=cart).values_list('id', 'dish_desc', 'dish_type__name')
        selected_combined_descriptions = []
        for di in selected_dishes:
            clean_desc = di[1].replace('\n', ' ').replace('\r', '')
            typename = di[2]
            combined = clean_desc + ' ' + typename
            selected_combined_descriptions.append(combined)

        cart_tfidf = tfidf.transform(selected_combined_descriptions)

        sim_scores = cosine_similarity(cart_tfidf, tfidf_matrix)

        # 取相似度排名前n的菜品，包括历史订单中和当前购物车中的菜品
        similar_indices = np.argsort(-sim_scores)[:, :n]
        similar_dish_indices = set(similar_indices.flatten())

        # 去掉购物车中已经选择的菜品
        selected_dish_ids = set([d[0] for d in selected_dishes])
        similar_dish_indices -= selected_dish_ids

        recommendations = Dish.objects.filter(id__in=similar_dish_indices)
        return recommendations.values()
    def get_recommendations_based_order(self, cart, user_id):
        # 从数据库中获取用户购买过的所有订单的订单号
        orders = Order.objects.filter(user_id=user_id).values_list('id', flat=True)
        # 获取所有订单中的菜品ID
        dish_ids = OrderInfo.objects.filter(order_id__in=orders).values_list('dish_id', flat=True)
        # 获取用户订单的属性信息，包括菜品描述和菜品类型
        purchased_dishes = Dish.objects.filter(id__in=dish_ids).values_list('id', 'dish_desc', 'dish_type__name')
        # 将所有菜品的描述信息和类型信息进行字符串拼接，并删除换行符
        combined_descriptions = []
        for di in purchased_dishes:
            clean_desc = di[1].replace('\n', ' ').replace('\r', '')
            typename = di[2]
            combined = clean_desc + ' ' + typename
            combined_descriptions.append(combined)

        # 初始化TfidfVectorizer，将所有菜品的描述信息与类型信息转换为TF-IDF向量
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(combined_descriptions)

        # 获取用户的购物车内菜品信息，包括菜品ID，菜品描述和菜品类型
        selected_dishes = Dish.objects.filter(id__in=cart).values_list('id', 'dish_desc', 'dish_type__name')

        # 将所有菜品的描述信息和类型信息进行字符串拼接，并删除换行符
        selected_combined_descriptions = []
        for di in selected_dishes:
            clean_desc = di[1].replace('\n', ' ').replace('\r', '')
            typename = di[2]
            combined = clean_desc + ' ' + typename
            selected_combined_descriptions.append(combined)

        # 计算购物车内菜品的TF-IDF向量
        cart_tfidf = tfidf.transform(selected_combined_descriptions)

        # 计算购物车内菜品与用户购买过的所有菜品之间的余弦相似度
        sim_scores = cosine_similarity(cart_tfidf, tfidf_matrix)

        # 获取与购物车内菜品相似度最高的前n个用户的所有订单
        n = 2

        # 将用户 ID 和索引之间建立映射关系
        user_data = User.objects.all().values('id')
        print('user_data',user_data)
        id_to_index = {u['id']: i for i, u in enumerate(user_data)}

        user_index = id_to_index[user_id]  # 将用户 ID 转换成相应的索引号（因为索引从0开始）
        user_sim_scores = sim_scores[user_index]  # 取出目标用户与所有用户的相似度得分
        similar_user_indices = user_sim_scores.argsort()[:-n - 1:-1]  # 获取前 N 个相似用户的索引值
        print('similar_user_indices',similar_user_indices)
        similar_user_ids = [user_data[int(index)]['id'] for index in similar_user_indices]  # 将索引值映射回对应的用户 ID

        similar_user_orders = Order.objects.filter(user_id__in=similar_user_ids).values_list('id', flat=True)
        print("similar_user_orders:", similar_user_orders)

        # 获取这些订单中的所有菜品ID
        similar_user_dish_ids = OrderInfo.objects.filter(order_id__in=similar_user_orders).values_list(
            'dish_id', flat=True)

        # 获取这些菜品的属性信息，包括菜品描述和菜品类型
        similar_dishes = Dish.objects.filter(id__in=similar_user_dish_ids).values_list('id', 'dish_desc',
                                                                                       'dish_type__name')

        # 计算购物车内菜品和这些菜品之间的相似度
        selected_dish_ids = set([d[0] for d in selected_dishes])
        similar_dish_indices = set(d[0] for d in similar_dishes) - selected_dish_ids

        # 获取推荐结果，并返回
        recommendations = Dish.objects.filter(id__in=similar_dish_indices)
        return recommendations.values()

    # 没有订单
    def get_recommendatsion_based_cart(self, cart):
        # 获取所有菜品的id、描述信息和类型
        dishes = Dish.objects.values('id', 'dish_desc', 'dish_type__name')
        # 记录菜品的id和索引之间的对应关系
        # dish_id_to_index = {dish['id']: index for index, dish in enumerate(dishes)}
        # 获取所有菜品的描述信息，并将回车等特殊符号替换为' '
        descriptions = []
        for di in dishes:
            des = di['dish_desc'].replace('\n', ' ').replace('\r', '') + ' ' + di['dish_type__name']
            descriptions.append(des)

        # 初始化TfidfVectorizer，将所有菜品的描述信息转换为TF-IDF向量
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(descriptions)
        # 根据购物车内的菜品ID，获取相应的属性信息
        selected_dishes = Dish.objects.filter(id__in=cart).values('dish_desc', 'dish_type__name')
        # 将购物车内每个菜品的描述信息进行预处理
        selected_descriptions = []
        for de in selected_dishes:
            des = de['dish_desc'].replace('\n', ' ').replace('\r', '') + ' ' + de['dish_type__name']
            selected_descriptions.append(des)
        # 计算购物车内菜品的TF-IDF向量
        cart_tfidf = tfidf.transform(selected_descriptions)
        # 计算购物车内菜品与其他菜品之间的余弦相似度
        sim_scores = cosine_similarity(cart_tfidf, tfidf_matrix)
        # 获取与购物车内菜品相似度最高的前n个菜品的索引
        n = 20
        similar_dish_indices = sim_scores[0].argsort()[:-n - 1:-1]
        # 将菜品的索引转换为菜品的id
        similar_dish_ids = [dishes[int(index)]['id'] for index in similar_dish_indices]
        # 过滤掉购物车中已经选中的菜品
        similar_dish_ids = [dish_id for dish_id in similar_dish_ids if dish_id not in cart]
        # 查询数据库获取推荐菜品的详细信息
        similar_dishes = Dish.objects.filter(id__in=similar_dish_ids)
        # 返回推荐结果
        # print('cart', cart)
        # print('returnCart', similar_dish_ids)
        # print('des', descriptions[0])
        # print('cartDes', selected_descriptions[0])
        return similar_dishes.values()

    # 用户有过点餐记录,且订单数大于20
    def get_recommendations_based_history(self, cart, user_id):
        # 获取用户购买过的所有订单的订单号
        orders = Order.objects.filter(user_id=user_id).values_list('id', flat=True)
        # 获取所有订单中的菜品ID
        dish_ids = OrderInfo.objects.filter(order_id__in=orders).values_list('dish_id', flat=True)
        # 获取所有菜品的属性信息
        purchased_dishes = Dish.objects.filter(id__in=dish_ids).values_list('id', 'dish_desc')
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform([d[1] for d in purchased_dishes])

        # 根据购物车内的菜品，获取相应的属性信息
        selected_dishes = Dish.objects.filter(id__in=cart).values_list('id', 'dish_desc')
        # 计算购物车内菜品的TF-IDF向量
        cart_tfidf = tfidf.transform([d[1] for d in selected_dishes])
        # 计算购物车内菜品和用户购买过的所有菜品之间的余弦相似度
        sim_scores = cosine_similarity(cart_tfidf, tfidf_matrix)
        # 获取与购物车内菜品相似度最高的前n个菜品
        n = 20
        sim_scores = sim_scores[0]
        similar_dish_indices = sim_scores.argsort()[:-n:-1]
        similar_dish_ids = [purchased_dishes[int(i)][0] for i in similar_dish_indices]

        similar_dishes = Dish.objects.filter(id__in=similar_dish_ids)
        return similar_dishes.values()


# 口味列表
class getFlavor(View):
    def get(self, request):
        flavor_list = []
        flavors = DishFlavor.objects.all()
        for flavor in flavors:
            obj = {
                "id": flavor.id,
                "name": flavor.name,
                "desc": flavor.desc
            }
            flavor_list.append(obj)
        count = flavors.count()
        return JsonResponse({"flavorList": flavor_list, "total": count})
