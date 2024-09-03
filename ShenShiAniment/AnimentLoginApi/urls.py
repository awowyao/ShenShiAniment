from django.urls import path
from AnimentLoginApi.views import *

urlpatterns = [
    path('Login', AnimentUserLogin.as_view()),
    path('Sign', AnimentUserSign.as_view()),
    path('GetUserMsg', GetUserMsg.as_view()),
    path('UpUserCode', UpUserCode.as_view())
]