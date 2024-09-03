from django.shortcuts import render

# Create your views here.
from AnimentLoginApi.models import *
from rest_framework.views import APIView
from django.http import HttpResponseForbidden, JsonResponse
import datetime, json, re
import random
import hashlib
from django.core.cache import cache

def Md5(str):
  md5 = hashlib.md5()  # 创建md5对象
  # 此处必须声明encode
  # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
  md5.update(str.encode(encoding='utf-8'))
  # 把输入的旧密码装换为md5格式
  result = md5.hexdigest()
  # 返回加密结果
  return result


class AnimentUserLogin(APIView):
    authentication_classes = []
    def post(self, request):
        # user = request.POST.get('username')
        try:
            UserData = json.loads(request.body)
            # print(data)
            userID = UserData['userName']
            userPwd = str(UserData['userPwd'])
            # 密码正则
            pwdRe = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d.#,!]{8,}$'
            userIDRe = '^.*(?=.*[@$%^&*()_+?><:"])[@$%^&*()_+?><:"|/=-]{1,}$'
            if not re.findall(pwdRe, userPwd) or re.findall(userIDRe,userID):
                return JsonResponse({'code': 401, 'msg': '错误'}, status=401)
            userPwd = Md5(userPwd)
            UserData = users_table.objects.filter(user_name=userID, user_pwd=userPwd).first()
            if not UserData:
                # raise exceptions.AuthenticationFailed('403-请登录')
                return JsonResponse({'code': 403, 'msg': '密码错误'}, status=403)

            # 为用户创建token
            zm_list = ['a','b','c','d','e','f','g','h','i','j','k','l','n','m','o','p','q','r','s','t','1','2','3']
            mi = random.sample(zm_list, 5)
            token = Md5(str(userID) + userPwd + ''.join(mi))
            # 存在就更新，不存在就创建
            now_time = datetime.datetime.now()
            UserToken.objects.update_or_create(user=UserData, defaults={'token': token, 'time': now_time})

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
            else:
                ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip


            UserData.user_last_login = {'time': now_time.strftime('%Y-%m-%d %H:%M:%S'), 'ip': ip}
            UserData.save()
            # 存入redis
            # cache.set(token, userID, timeout=60*60*12)

            UserMsg = {'code': 201, 'msg': '登录成功', 'token': token}

        except Exception as e:
            UserMsg = {'code': 401, 'msg': '传参出错'}
            return JsonResponse(UserMsg, status=401)

        return JsonResponse(UserMsg)

class AnimentUserSign(APIView):
    authentication_classes = []
    def post(self, request):
        UserData = json.loads(request.body)
        userID = UserData['userName']
        userPwd = str(UserData['userPwd'])
        userEmail = UserData['userEmail']
        pwdRe = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d.#,!]{8,}$'
        userIDRe = '^.*(?=.*[@$%^&*()_+?><:"])[@$%^&*()_+?><:"|/=-]{1,}$'

        if (not re.findall(pwdRe, userPwd)) or re.findall(userIDRe, userID):
            return JsonResponse({'code': 401, 'msg': '错误'}, status=401)
        elif users_table.objects.filter(user_name=userID):
            return JsonResponse({'code': 401, 'msg': '用户名已存在'}, status=401)
        elif users_table.objects.filter(user_email=userEmail):
            return JsonResponse({'code': 401, 'msg': '邮箱已存在'}, status=401)
        else:
            userPwd = Md5(userPwd)

            # userNickname = request.POST.get('userNickname')
            # userCover = request.POST.get('userCover')
            # userSex = request.POST.get('userSex')
            #
            # userMobile = request.POST.get('userMobile')
            # userAddress = request.POST.get('userAddress')
            userSignTime = datetime.datetime.now()
            uploadUser = users_table(user_name=userID,
                        user_pwd=userPwd,
                        # user_nickname=userNickname,
                        # user_cover=userCover,
                        # user_sex=userSex,
                        user_email=userEmail,
                        # user_Mobile=userMobile,
                        # user_address=userAddress,
                        user_sign_time=userSignTime)
            uploadUser.save()
            return JsonResponse({'code': 201, 'msg': '注册成功'}, status=201)

class GetUserMsg(APIView):
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        TokenObj = UserToken.objects.get(token=Usertoken)
        UserMsg = TokenObj.user
        UserDic = {'userName':UserMsg.user_name,
                   'userEmail':UserMsg.user_email,
                   'user_nickname':UserMsg.user_nickname,
                   'user_cover':UserMsg.user_cover}
        return JsonResponse(UserDic)

class UpUserCode(APIView):
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        TokenObj = UserToken.objects.get(token=Usertoken)
        User = TokenObj.user
        zm_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'n', 'm', 'o', 'p', 'q', 'r', 's', 't',
                   '1', '2', '3', '4', 'ad', 'fv', 'qw', 'hj', 'zz']
        mi = random.sample(zm_list, 5)
        token = Md5(str(User.user_name) + User.user_pwd + ''.join(mi))
        # 存在就更新，不存在就创建
        now_time = datetime.datetime.now()
        UserToken.objects.update_or_create(user=User, defaults={'token': token, 'time': now_time})

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
        User.user_last_login = {'time': now_time.strftime('%Y-%m-%d %H:%M:%S'), 'ip': ip}
        User.save()
        UserMsg = {'code': 201, 'msg': '登录成功', 'token': token}
        return JsonResponse({'msg':'更新成功', 'token': token}, status=201)