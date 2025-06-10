import json

from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
# from django.contrib.sessions.models import Session
from .models import User, ImgSave
from django.core.mail import send_mail
import random
from datetime import datetime, timedelta

from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


# Create your views here.
# 登录逻辑
# class Login(View):

# def post(self, request):
# data = json.loads(request.body)
# print(data)
# username = data.get('username')
# password = data.get('password')
# print(username, password)
# print(request.POST.get('username'),request.POST.get('password'))
# return JsonResponse({'status':'success'})
# try:
#     sessionid = request.headers.get('Authorization').split(' ')[1]
#
# except Exception as e:
#     print(e)
# if len(sessionid) > 0:
#     try:
#         session = Session.objects.get(session_key=sessionid)
#
#         print('当前请求中有sessionid', session)
#     except Session.DoesNotExist:
#         session = None
#     if session is not None:
#         print('当前sessionid正确', session)
#         user_data = session.get_decoded()
#         return JsonResponse({'status': 'sessionid正确，', 'data': user_data})
#     else:
#         print('当前sessionid错误')
#         return JsonResponse({'status': 'sessionid错误', 'data': 0})
# else:
#     data = json.loads(request.body)
#     name = data.get('username')
#     password = data.get('password')
#     print(f'username:{name},password:{password}')
#     if name and password:
#         request.session.save()
#         request.session['info'] = {'name': name, 'password': password}
#         session_id = request.session.session_key
#         print(request.session.session_key)
#         response = JsonResponse({'status': '注册成功', 'sessionid': session_id})
#         # response['Access-Control-Allow-Credentials'] = 'true'
#         # response['Access-Control-Allow-Origin'] = '*'
#         return response
#     else:
#         print('用户名或密码为空')
#         return JsonResponse({'status': '内容不能为空'})

# def post(self, request):
#     session_key = request.COOKIES.get('sessionid')
#     print('当前的sessionKey',session_key)
#     if session_key is not None:
#         print('当前的session不为空')
#         try:
#             session = Session.objects.get(session_key=session_key)
#         except Session.DoesNotExist:
#             session = None
#         if session is not None:
#             print('当前sessionid正确')
#             return JsonResponse({'status': '登陆成功', 'data': 'zs'})
#         else:
#             return JsonResponse({'status': '不正确'})
#     else:
#         data = json.loads(request.body)
#         print(data, type(data))
#         name = data.get('username')
#         password = data.get('password')
#         print('新用户来了', name, password)
#
#         # if name and password:
#         request.session['info'] = {'name': name, 'password': password}
#         request.session.set_expiry(86400)
#         session_key = request.session.session_key
#         print('当前用户的sessionkey',session_key)
#         response = HttpResponse()
# response = JsonResponse({'status': 'YES'})
# 设置允许使用cookie
# response['Access-Control-Allow-Credentials'] = 'true'
# response['Access-Control-Allow-Origin'] = '*'
# response.set_cookie('sessionid', session_key, max_age=86400,)
# return response


class Login(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(username, password)
        obj = {'username': username, 'password': password}

        if username and password:
            res = User.objects.filter(**obj).exists()
            if res:
                request.session.save()
                request.session['info'] = obj
                # 设置过期时间，设置一周内过期
                expires = datetime.now() + timedelta(days=7)
                request.session.set_expiry(expires)
                session_id = request.session.session_key
                print(session_id)
                response = JsonResponse({'status': 'success', 'sessionid': session_id}, status=200)
                return response

            else:
                return JsonResponse({'status': 'error', 'msg': '账号或密码错误'}, status=401)
        else:
            return HttpResponseBadRequest('请检查相关字段')


# 注册逻辑
class Register(View):

    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')
        gender = data.get('gender')
        print(type(gender))
        integral = 0
        print(username, password, phone, gender, integral)
        if User.objects.filter(phone=phone).exists():
            return JsonResponse({'status': 'error', 'msg': '该手机号已被注册'}, status=400)
        if username and password and phone:
            obj = {'username': username, 'password': password, 'phone': phone, 'gender': gender, 'integral': integral}
            user = User(**obj)
            user.save()
            return JsonResponse({'status': 'success', 'data': obj})
        else:
            return JsonResponse({'error': 'Missing required field'}, status=400)


# 找回密码
class FindPwd(View):
    def _get_code(self, length=6):

        # 随机选择字符集合
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        # 生成随机字符串
        code = ''.join(random.choice(chars) for i in range(length))
        return code

    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        phone = data.get('phone')
        email = data.get('email')
        default_code = '8848'
        # 如果code字段存在，那么就是修改密码，则有newpwd
        if 'code' in data.get('code'):
            newpwd = data.get('newpwd')
            code = data.get('code')
            if code == default_code:
                try:
                    User.objects.filter(username=username, phone=phone).update(password=newpwd)
                    return JsonResponse({'status': 'success'}, status=200)
                except Exception  as e:
                    return JsonResponse({'status': 'error', 'msg': '修改失败'}, status=400)
            else:
                return JsonResponse({'status': 'error', 'msg': '验证码错误'}, status=400)
        # 如果不存在验证码字段，则说明是获取验证码
        else:
            default_code = self._get_code(6)
            res = send_mail("飞飞点餐", f"您的验证码是:{default_code},验证码五分钟内有效", "zx529213@qq.com", [email])
            # res大于0则说明发送成功
            if res > 0:
                return JsonResponse({'status': 'success'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'msg': '验证码发送失败'}, status=400)


class index(View):
    def get(self, request):
        # return HttpResponse('欢迎光临，这是index页面')
        return JsonResponse({"data": {"name": "zs"}}, status=200)


class SaveImg(View):
    def post(self, request):
        # media下面的文件夹名字，可以不写，不写就默认是在media文件夹下
        file_name = 'notices/'
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        # print(title, description, type(image))
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,file_name))
        img_name = fs.save(image.name, image)

        #  /ip:port + /media/ + /notices/ + a.png
        img_url = '127.0.0.1:8000'+settings.MEDIA_URL+file_name+img_name
        print(img_url)
        try:
            ImgSave.objects.create(title=title, description=description, imgURL=img_url)
            return JsonResponse({'status':'success','url':img_url},status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', "msg": e}, status=400)
