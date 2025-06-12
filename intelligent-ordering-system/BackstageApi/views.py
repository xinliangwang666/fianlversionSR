import json
import pprint

from django.http import JsonResponse
from django.views import View
from django.contrib.sessions.models import Session
from .models import Admin, Notice, Dish, DishType, DishFlavor, Order, OrderInfo
from ForegroundApi.models import User
from datetime import datetime, timedelta
from django.utils.decorators import method_decorator
# 分页处理
from django.core.paginator import Paginator
# 导入时间格式化
from django.utils import timezone
# 添加信息的异常类
from django.db.utils import IntegrityError

from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


# Create your views here.
# 自定义装饰器


# 管理员或用户登录
class Login(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        role_str = data.get('role')

        try:
            role = int(role_str)
        except (TypeError, ValueError):
            return JsonResponse({'status': 'error', 'msg': "无效的角色类型"}, status=400)

        # 验证角色范围
        if role not in [0, 1, 2]:
            return JsonResponse({'status': 'error', 'msg': "无效的角色值"}, status=400)

        obj = {'name': username, 'password': password, 'role': role}
        res = Admin.objects.filter(**obj).exists()

        if res:
            print('当前用户信息正确', obj)
            request.session.save()
            request.session['info'] = obj
            expires = datetime.now() + timedelta(days=7)
            request.session.set_expiry(expires)
            session_id = request.session.session_key
            response = JsonResponse({'status': 'success', 'sessionid': session_id}, status=200)
            return response
        else:
            return JsonResponse({'status': 'error', 'msg': "账户名或密码错误"}, status=401)


# 自定义装饰器
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
                # login_user = user_data['info']['role']
                # if request.method!='GET'
                #     opear_role = json.loads()
                # print(f'当前用户:{user_data.name},角色:{user_data.role}')
                print('当前登录用户', user_data['info'])
                return func(request, *args, **kwargs)
            else:
                return JsonResponse({'status': 'error', 'msg': "非法访问"}, status=401)
        else:
            return JsonResponse({'status': 'error'}, status=401)

    return wrapper


# 商家管理
class AdminInfo(View):

    # 获取当前所有商家以及admin信息
    @method_decorator(check_session_id)
    def get(self, request):
        print('触发了get请求')
        user_list = []
        # superAdmin不进行展示
        users = Admin.objects.exclude(role=0)
        for user in users:
            obj = {'id': user.id, 'name': user.name, 'password': user.password, 'phone': user.phone, 'role': user.role}
            user_list.append(obj)
        return JsonResponse({'status': 'success', 'data': {
            "admin_list": user_list
        }}, status=200)

    # 添加一条商家信息
    @method_decorator(check_session_id)
    def post(self, request):
        data = json.loads(request.body)
        name = data.get('account')
        password = data.get('password')
        phone = data.get('phone')
        # 当前添加角色的role
        role = data.get('role', 2)
        # 获取当前sessionid中与之对应的roleid，来判断权限够不够
        session_id = request.headers.get('Authorization', False).split(' ')[1]
        session = Session.objects.get(session_key=session_id)
        # 当前请求对象的role
        author_id = int(session.get_decoded()['info']['role'])
        # 只有superAdmin才能添加管理员，管理员可以添加商家
        print(f'当前登录权限：{author_id}，当前添加的角色权限{role}')
        if author_id >= role:
            return JsonResponse({'status': 'error', 'msg': '权限不够'}, status=401)

        obj = {'name': name, 'password': password, 'phone': phone, 'role': role}
        try:
            Admin.objects.create(**obj)
            return JsonResponse({'status': 'success', "msg": "添加成功"}, status=200)
        except IntegrityError as e:
            print('管理员创建失败：', e)
            return JsonResponse({'status': 'error', 'msg': e}, status=401)

    # 修改商家信息
    @method_decorator(check_session_id)
    def put(self, request):
        data = json.loads(request.body)
        id = data.get('id')
        res = Admin.objects.filter(id=id).first()

        # 当前请求者的role
        session_id = request.headers.get('Authorization', False).split(' ')[1]
        session = Session.objects.get(session_key=session_id)
        author_id = session.get_decoded()['info']['role']
        if res:
            roleid = res.role
        else:
            return JsonResponse({'status': 'error', 'msg': '角色不存在'}, status=400)
        if author_id < roleid:
            name = data.get('name')
            password = data.get('password')
            phone = data.get('phone')
            role = data.get('role')
            obj = {'name': name, 'password': password, 'phone': phone, 'role': role}
            res = Admin.objects.filter(id=id).update(**obj)
            if res > 0:
                return JsonResponse({'status': 'success', 'data': obj}, status=200)
            else:
                return JsonResponse({'status': 'error', 'msg': '更新失败'}, status=400)

        else:
            return JsonResponse({'status': 'error', 'msg': '权限不够'}, status=401)

    # 删除商家
    @method_decorator(check_session_id)
    def delete(self, request):
        data = json.loads(request.body)
        id = data.get('id')
        admin = Admin.objects.filter(id=id).first()
        if admin:
            admin.delete()
            print(admin)
            name = admin.name
            return JsonResponse({'status': 'success', 'data': name}, status=200)
        else:
            return JsonResponse({'status': 'error', 'msg': '删除失败'}, status=400)


# 用户管理
class UserInfo(View):
    def get(self, request):
        user_id = request.GET.get('id')
        # 如果是有id存在，则说明是获取某个用户的具体信息，否则就是获取全部列表
        if user_id is not None:
            res = User.objects.filter(id=user_id)
            if res.exists():
                user = res.first()
                print(user)
                obj = {
                    "id": user.id,
                    "name": user.name,
                    "password": user.password,
                    "gender": user.gender,
                    "integral": user.integral,
                    "phone": user.phone,
                    "email": user.email,
                    "avatar_img": user.avatar_url,
                    "addr": user.addr
                }
                return JsonResponse({"data": obj})
            else:
                return JsonResponse({"status": "error", "msg": "该用户不存在"})
        else:
            user_list = []
            page_num = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 10)

            users = User.objects.all()
            count = users.count()
            paginator = Paginator(users, page_size)
            page = paginator.get_page(page_num)
            for user in page:
                obj = {
                    'id': user.id,
                    'avatar_url': user.avatar_url,
                    'name': user.name,
                    'password': user.password,
                    'phone': user.phone,
                    'gender': user.gender,
                    'integral': user.integral,
                    'email': user.email,
                    'addr': user.addr
                }
                user_list.append(obj)
            return JsonResponse({
                "data": {
                    "page_num": page_num,
                    "page_size": page_size,
                    "total": count,
                    "user_list": user_list
                }
            })

    @method_decorator(check_session_id)
    def put(self, request):
        # 获取当前用户的角色
        session_id = request.headers.get('Authorization').split(' ')[1]
        session = Session.objects.get(session_key=session_id)
        current_role = session.get_decoded()['info']['role']

        data = json.loads(request.body)
        user_id = data.get('user_id')
        name = data.get('name')
        password = data.get('password')
        gender = data.get('gender')
        integral = data.get('integral')
        phone = data.get('phone')
        email = data.get('email')
        addr = data.get('addr')

        # 创建基本更新字段
        obj = {
            "password": password,
            "gender": gender,
            "integral": integral,
            "phone": phone,
            "email": email,
        }

        # 管理员和超级管理员可以修改用户名和地址
        if current_role in [0, 1]:  # 0是超级管理员，1是管理员
            if name is not None:
                obj["name"] = name
            if addr is not None:
                obj["addr"] = addr
        elif addr is not None:
            return JsonResponse({"status": "error", "msg": "商家不能修改用户地址"}, status=403)

        user = User.objects.filter(id=user_id)
        if user.exists():
            try:
                user.update(**obj)
                return JsonResponse({"status": "success"})
            except Exception as e:
                return JsonResponse({"status": "error", "msg": str(e)}, status=400)
        else:
            return JsonResponse({"status": "error", "msg": "用户不存在"}, status=400)

    @method_decorator(check_session_id)
    def delete(self, request):
        id = json.loads(request.body).get('id')
        user = User.objects.filter(id=id).first()
        if user:
            name = user.name
            user.delete()
            return JsonResponse({'status': 'success', 'data': name, 'count': 1})
        else:
            return JsonResponse({'status': 'error', 'msg': '用户不存在', 'count': 0}, status=400)


# 公告管理
class NoticeInfo(View):
    # 使用自定义装饰器来判断是否存在sessionid
    @method_decorator(check_session_id)
    def get(self, request):
        notice_list = []
        notices = Notice.objects.all()
        count = notices.count()
        for notice in notices:
            obj = {
                'id': notice.id,
                'title': notice.title,
                'description': notice.description,
                'pub_date': notice.pub_date,
                'img_url': notice.imgURL
            }
            notice_list.append(obj)
        return JsonResponse({
            'total': count,
            'noticeList': notice_list
        })

    @method_decorator(check_session_id)
    def post(self, request):
        print('进入了post请求')
        # media下面的文件夹名字，可以不写，不写就默认是在media文件夹下
        file_name = 'notices/'
        print(request.POST)
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        image = request.FILES.get('image')
        print(title, desc, type(image))
        # # 这里的location就表示存储路径类似于 /media/notices
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, file_name))
        img_name = fs.save(image.name, image)

        #  /ip:port + /media/ + /notices/ + a.png
        img_url = 'http://127.0.0.1:8000' + settings.MEDIA_URL + file_name + img_name
        try:
            Notice.objects.create(title=title, description=desc, imgURL=img_url)
            return JsonResponse({'status': 'success', 'url': img_url}, status=200)
        except IntegrityError:
            return JsonResponse({'status': 'error', "msg": "添加失败"}, status=400)

    @method_decorator(check_session_id)
    def delete(self, request):
        data = json.loads(request.body)
        print(data)
        notice_id = data.get('id')
        print(notice_id, type(notice_id))

        notice = Notice.objects.filter(id=notice_id)

        if notice:
            name = notice.first().title
            notice.delete()
            print('执行了删除操作,删除成功')
            return JsonResponse({'status': 'success', 'data': name})
        else:
            return JsonResponse({'status': 'error', 'msg': '用户不存在'}, status=400)


# 菜品管理
class DishInfo(View):
    @method_decorator(check_session_id)
    def get(self, request):
        id = request.GET.get('id')
        if id is not None:
            dish = Dish.objects.filter(id=id).first()
            obj = {
                'id': dish.id,
                'name': dish.dish_name,
                'price': dish.dish_price,
                'desc': dish.dish_desc,
                'cover': dish.dish_img,
                'order_count': dish.order_count,
                'type': dish.dish_type_id
            }
            return JsonResponse({"DishInfo": obj})

        # 如果没有传入id，则进行分页处理
        page_num = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        dishes = Dish.objects.select_related('dish_type').all()
        count = dishes.count()
        paginator = Paginator(dishes, page_size)
        page = paginator.get_page(page_num)
        dish_list = []
        for dish in page:
            obj = {
                'id': dish.id,
                'name': dish.dish_name,
                'price': dish.dish_price,
                'desc': dish.dish_desc,
                'cover': dish.dish_img,
                'order_count': dish.order_count,
                'type': dish.dish_type.name
            }
            dish_list.append(obj)
        return JsonResponse({
            "data": {"dish_list": dish_list, "page_num": page_num, "page_size": page_size, "dish_count": count}
        })

    @method_decorator(check_session_id)
    def post(self, request):
        print('进入了post请求')
        # media下面的文件夹名字，可以不写，不写就默认是在media文件夹下
        file_name = 'dishes/'
        name = request.POST.get('dish_name')
        price = request.POST.get('dish_price')
        desc = request.POST.get('dish_desc')
        # order_count = request.POST.get('order_count')
        # flavor_id = request.POST.get('flavor_id')
        type_id = request.POST.get('type_id')
        image = request.FILES.get('dish_img')
        print(name, price, type_id, type(image))
        # # 这里的location就表示存储路径类似于 /media/notices
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, file_name))
        img_name = fs.save(image.name, image)
        print('media_root', settings.MEDIA_ROOT)
        print('media_url', settings.MEDIA_URL)
        print(file_name, image.name, image)
        #  /ip:port + /media/ + /notices/ + a.png
        img_url = 'http://127.0.0.1:8000' + settings.MEDIA_URL + file_name + img_name
        try:
            Dish.objects.create(dish_name=name, dish_price=price, dish_desc=desc, order_count=0,
                                dish_type_id=type_id, dish_img=img_url)
            return JsonResponse({'status': 'success', 'url': img_url}, status=200)
        except IntegrityError:
            print('请检查菜品typeid是否正确')
            return JsonResponse({'status': 'error', "msg": "添加失败"}, status=400)

    @method_decorator(check_session_id)
    def delete(self, request):
        data = json.loads(request.body)
        id = data.get('id')
        dish = Dish.objects.filter(id=id)
        if dish.exists():
            name = dish.first().dish_name
            dish.delete()
            print(f'删除了{name}')
            return JsonResponse({"status": "success", "msg": f"{name}已被删除"})
        else:
            return JsonResponse({"status": "success", "msg": "id不存在"}, status=400)


# 菜品类别（炒菜 面食……)
class DishTypeInfo(View):
    @method_decorator(check_session_id)
    def get(self, request):
        dish_types = DishType.objects.all()
        count = dish_types.count()
        type_list = []
        for types in dish_types:
            obj = {
                "id": types.id,
                "name": types.name,
                "desc": types.desc
            }
            type_list.append(obj)
        return JsonResponse({"status": "success", "data": {"dishType": type_list, "total": count}})

    def post(self, request):
        data = json.loads(request.body)
        name = data.get('name', '默认')
        desc = data.get('desc')
        try:
            DishType.objects.create(name=name, desc=desc)
            return JsonResponse({'status': 'success', 'msg': '添加成功'})
        except Exception as e:
            return JsonResponse({"status": "success", "msg": "添加失败"}, status=400)

    @method_decorator(check_session_id)
    def delete(self, request):
        data = json.loads(request.body)
        id = data.get('id')
        flavor = DishType.objects.filter(id=id)
        if flavor.exists():
            name = flavor.first().name
            flavor.delete()
            return JsonResponse({"status": "success", "msg": f"已删除{name}"})
        else:
            return JsonResponse({"status": "success", "msg": "id不存在"}, status=400)


# 菜品口味 酸辣 香辣
class DishFlavorInfo(View):
    # @method_decorator(check_session_id)
    def get(self, request):
        dish_flavors = DishFlavor.objects.all()
        count = dish_flavors.count()
        flavor_list = []
        for flavor in dish_flavors:
            obj = {
                "id": flavor.id,
                "name": flavor.name,
                "desc": flavor.desc
            }
            flavor_list.append(obj)
        return JsonResponse({"status": "success", "data": {"dishFlavor": flavor_list, "total": count}})

    @method_decorator(check_session_id)
    def post(self, request):
        data = json.loads(request.body)
        name = data.get('name', '默认')
        desc = data.get('desc')
        try:
            DishFlavor.objects.create(name=name, desc=desc)
            return JsonResponse({'status': 'success', 'msg': '添加成功'})
        except Exception as e:
            return JsonResponse({"status": "success", "msg": "添加失败"}, status=400)

    @method_decorator(check_session_id)
    def delete(self, request):
        data = json.loads(request.body)
        id = data.get('id')
        print(id)
        flavor = DishFlavor.objects.filter(id=id)
        if flavor.exists():
            name = flavor.first().name
            flavor.delete()
            print(f'{name}删除成功')
            return JsonResponse({"status": "success", "msg": f"已删除{name}"})
        else:
            print('id不存在')
            return JsonResponse({"status": "success", "msg": "id不存在"}, status=400)


# 订单管理


class OrderManage(View):
    @method_decorator(check_session_id)
    def get(self, request):
        order_info = []
        # 使用 `select_related` 关联查询用户、口味，并获取 `status` 字段
        orders = Order.objects.select_related('user', 'flavor') \
            .values('id', 'user__name', 'flavor__name', 'total', 'create_time', 'status') \
            .order_by('-create_time')

        # 以下代码缩进至 `get` 方法内（注意缩进层级！）
        count = orders.count()
        page_num = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(orders, page_size)
        page = paginator.get_page(page_num)

        for order in page:
            obj = {
                'order_id': order['id'],
                'user_name': order['user__name'],
                'order_flavor': order['flavor__name'],
                'order_time': order['create_time'],
                'order_total_price': order['total'],
                'status': order['status'],  # 新增状态字段
                'dishes': []
            }
            # 获取订单对应的菜品信息
            orderinfo_set = OrderInfo.objects.filter(order_id=order['id'])
            for orderinfo in orderinfo_set:
                dish_obj = {
                    'dish_id': orderinfo.dish_id,
                    'dish_name': orderinfo.dish.dish_name,
                    'dish_price': orderinfo.price,
                    'dish_count': orderinfo.count,
                    'dish_total_price': orderinfo.dish_total_price,
                    'dish_img': orderinfo.dish.dish_img
                }
                obj['dishes'].append(dish_obj)
            order_info.append(obj)  # 注意：这里用 append 而非 insert(0)，避免顺序颠倒

        return JsonResponse({  # return 语句缩进与方法体一致
            "data": {
                "order_list": order_info,
                "page_size": page_size,
                "page_num": page_num,
                "order_count": count
            }
        })

    @method_decorator(check_session_id)
    def delete(self, request):
        """处理订单删除请求"""
        try:
            data = json.loads(request.body)
            order_id = data.get('id')

            if not order_id:
                return JsonResponse({'status': 'error', 'msg': '缺少订单ID'}, status=400)

            # 检查订单是否存在
            order = Order.objects.filter(id=order_id).first()
            if not order:
                return JsonResponse({'status': 'error', 'msg': '订单不存在'}, status=404)

            # 删除订单（级联删除 OrderInfo 记录）
            order.delete()
            return JsonResponse({'status': 'success', 'msg': '订单删除成功'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'msg': '请求体格式错误'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'msg': str(e)}, status=500)

    @method_decorator(check_session_id)
    def put(self, request):
        try:
            data = json.loads(request.body)
            order_id = data.get('id')
            action = data.get('action')  # accept/reject/complete

            # 校验订单是否存在
            order = Order.objects.filter(id=order_id).first()
            if not order:
                return JsonResponse({'status': 'error', 'msg': '订单不存在'}, status=404)

            # 状态转换映射
            status_map = {
                'accept': 'accepted',
                'reject': 'rejected',
                'complete': 'completed'
            }
            new_status = status_map.get(action)

            if not new_status:
                return JsonResponse({'status': 'error', 'msg': '无效操作'}, status=400)

            # 状态校验（示例：已支付订单才能接单/拒单，已接单才能完成）
            if new_status == 'accepted' and order.status != 'paid':
                return JsonResponse({'status': 'error', 'msg': '订单未支付，无法接单'}, status=400)
            if new_status == 'completed' and order.status != 'accepted':
                return JsonResponse({'status': 'error', 'msg': '订单未接单，无法完成'}, status=400)

            # 更新订单状态
            order.status = new_status
            order.save()

            return JsonResponse({
                'status': 'success',
                'msg': '操作成功',
                'new_status': order.get_status_display()  # 返回中文状态
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'msg': '请求体格式错误'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'msg': str(e)}, status=500)

# 更新菜品
class UpdateDish(View):
    @method_decorator(check_session_id)
    def post(self, request):
        print('进入了post请求')
        # media下面的文件夹名字，可以不写，不写就默认是在media文件夹下
        file_name = 'dishes/'
        # data = json.loads(request.body)
        # print(request)
        id = request.POST.get('id')
        name = request.POST.get('dish_name')
        price = request.POST.get('dish_price')
        desc = request.POST.get('dish_desc')
        order_count = request.POST.get('order_count')
        type_id = request.POST.get('type_id')
        # order_count = request.POST.get('order_count')
        print(id, name, price, desc, order_count, type_id)
        if 'dish_img' in request.FILES:
            image = request.FILES.get("dish_img")
            print('需要更改图片')
            print(image)
            # return JsonResponse({"data": "Ok"})
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, file_name))
            img_name = fs.save(image.name, image)
            print(file_name, image.name, image)
            img_url = 'http://127.0.0.1:8000' + settings.MEDIA_URL + file_name + img_name

            dish = Dish.objects.filter(id=id)
            if dish.exists():
                dish.update(dish_name=name, dish_price=price, dish_desc=desc, order_count=order_count,
                            dish_type_id=type_id, dish_img=img_url)
                return JsonResponse({'status': 'success', }, status=200)
        else:
            dish = Dish.objects.filter(id=id)
            if dish.exists():
                dish.update(dish_name=name, dish_price=price, dish_desc=desc, order_count=order_count,
                            dish_type_id=type_id)
                return JsonResponse({"status": "success", "msg": "菜品信息更新成功"}, status=200)


# 是否有新订单
class NewOrder(View):
    @method_decorator(check_session_id)
    def get(self, request):
        last_id = int(request.GET.get('orderId'))
        print(last_id, type(last_id))
        # 判断是否为前端页面加载时请求
        if int(last_id) < 0:
            lastId = Order.objects.last().id
            return JsonResponse({"data": {"change": False, "lastId": lastId}})

        new_order = Order.objects.last().id
        # print('当前接收到的最后的订单id')
        # print(new_order, type(new_order))
        # print(last_id, type(last_id))
        print('收到的:',last_id,'当前的:',new_order)
        if new_order != last_id:
            print('当前订单信息有更新')
            # print(new_order.first().id)
            # newId = new_order.first().id
            return JsonResponse({"data": {"change": True, "lastId": new_order}})
        # order_data
        return JsonResponse({"data": {"change": False}})
