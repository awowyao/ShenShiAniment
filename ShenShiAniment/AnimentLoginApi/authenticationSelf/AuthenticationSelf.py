import datetime

from django.db import models
from django.http import JsonResponse
from rest_framework import exceptions

from rest_framework.exceptions import APIException
from rest_framework.authtoken.models import Token
from AnimentLoginApi.models import *
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
class AuthenticationSelf(BaseAuthentication):
    model = Token
    '''认证'''
    def authenticate(self,request):
        token = request.headers
        token = token['Token']
        if not token:
            raise exceptions.NotAuthenticated('请登录')
        # 查询认证信息
        token_obj = UserToken.objects.filter(token=token).first()
        # 开启redis
        # token_obj = cache.get(token)

        if not token_obj:
            raise exceptions.NotAuthenticated('认证失败')

        now_time = datetime.datetime.now()
        time = UserToken.objects.get(token=token).time
        delta = now_time - time
        if not delta < datetime.timedelta(minutes=60*6):
            raise exceptions.NotAuthenticated('认证过期')
        #在rest framework内部会将这两个字段赋值给request，以供后续操作使用
        return (token_obj, True)

    def authenticate_header(self, request):
        pass
