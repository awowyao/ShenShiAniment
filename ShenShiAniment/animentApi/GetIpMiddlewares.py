from django.utils.deprecation import MiddlewareMixin
import re
from django.http import JsonResponse,HttpResponse
from animentApi.models import user_visit
import datetime


class MD1(MiddlewareMixin):
    def process_request(self, request):  # process_request在视图之前执行
        # 获取ip
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        User_Agent = request.META.get('HTTP_USER_AGENT')

        if re.compile('python',re.S).findall(User_Agent):
            return HttpResponse('python应该没浏览器吧')


        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip

        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
        # and ip != '127.0.0.1'
        if (request.path_info == '/AinimentApi/getIndexAniment' or request.path_info == '/') :
            # 获取该IP上次访问时间
            user = user_visit.objects.filter(ip=ip).last()
            now_time = datetime.datetime.now()
            if user:
                Usertime = user.time
                delta = now_time - Usertime
                user.time = str(now_time)
                user.save()
                if delta < datetime.timedelta(seconds=1):
                    return JsonResponse({'msg':'访问速度过快等待两秒后重试','code':'410'}, status=410)
                user.visits_number += 1
                user.save()
            else:
                # 获取ip归属地
                # import requests
                # url = ''
                # r = requests.get(url.format(ip)).json()
                # text = ';'.join(r['data'])

                visit = user_visit(ip=ip,
                                   time=str(now_time),
                                   area="")
                visit.save()


    # process_response在视图之后
    def process_response(self,request, response): #基于请求响应
        return response