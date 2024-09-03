from django.db import models

# Create your models here.
from animentApi.models import Animent_table

# 用户信息
class users_table(models.Model):
    user_name = models.CharField(max_length=255)
    user_pwd = models.CharField(max_length=255)
    user_nickname = models.CharField(max_length=255, null=True)
    user_cover = models.CharField(max_length=255, null=True)
    user_sex = models.CharField(max_length=4, null=True)
    user_email = models.EmailField(null=True)
    user_Mobile = models.CharField(max_length=16,null=True)
    user_address = models.CharField(max_length=255, null=True)
    user_sign_time = models.CharField(max_length=50)
    user_last_login = models.CharField(max_length=255, null=True)
    user_score_dic = models.TextField(default='{}')
    user_lv = models.IntegerField(default=1)
    user_lv_msg = models.TextField(null=True)
    user_like_animent = models.ManyToManyField(Animent_table, related_name='userTable')

class UserCode(models.Model):
    user = models.OneToOneField(users_table, on_delete=models.CASCADE)
    commonlyCode = models.CharField(max_length=10, null=True)
    time = models.DateTimeField('创建时间', auto_now_add=True)

class UserToken(models.Model):
    user = models.OneToOneField(users_table, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    time = models.DateTimeField('创建时间', auto_now_add=True)