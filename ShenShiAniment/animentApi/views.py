import re

from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from AnimentLoginApi.models import users_table,UserToken
from django.core.paginator import Paginator
from rest_framework.views import APIView
from django.db.models import Q
# Create your views here.
from .aesJiaMi import *
import datetime, json
from ShenShiAniment.settings import videoPlayKey, videoPlayIv
from django.core.cache import cache
# 密钥
key = videoPlayKey
iv = videoPlayIv
aes = AEScryptor(key, AES.MODE_CBC, iv, paddingMode="ZeroPadding", characterSet='utf-8')

# 登录接口

# 注册接口

# 首页数据
def getAniment(request):
    data = Animent_table.objects.order_by('-uptime')[:12]
    all_data_list = [{  'id' : i.id,
                        'title':i.title,
                        'state':i.state,
                        'type':eval(i.type)[0],
                        'cover':i.cover,} for i in data]
    # 新番
    x_data = Animent_table.objects.order_by('-uptime').filter(state__contains='连载中')[:12]
    x_data_list = []
    for x in x_data:
        xdic = {
            'id': x.id,
            'title': x.title,
            'state': x.state,
            'type': eval(x.type)[0],
            'cover': x.cover,
        }
        x_data_list.append(xdic)
    china_data = Animent_table.objects.order_by('-uptime').filter(type__contains='国产剧')[:12]
    china_data_list = [{  'id' : i.id,
                        'title':i.title,
                        'state':i.state,
                        'type':eval(i.type)[0],
                        'cover':i.cover,} for i in china_data]

    europe_data = Animent_table.objects.order_by('-uptime').filter(type__contains='国产剧')[:12]
    europe_data_list = [{  'id' : i.id,
                        'title':i.title,
                        'state':i.state,
                        'type':eval(i.type)[0],
                        'cover':i.cover,} for i in europe_data]

    hong_kong_data = Animent_table.objects.order_by('-uptime').filter(type__contains='香港剧')[:12]
    hong_kong_data_list = [{  'id' : i.id,
                        'title':i.title,
                        'state':i.state,
                        'type':eval(i.type)[0],
                        'cover':i.cover,} for i in hong_kong_data]
    chine_zy_data = Animent_table.objects.order_by('-uptime').filter(type__contains='大陆综艺')[:12]
    chine_zy_data_list = [{  'id' : i.id,
                        'title':i.title,
                        'state':i.state,
                        'type':eval(i.type)[0],
                        'cover':i.cover,} for i in chine_zy_data]

    animent_data = Animent_table.objects.order_by('-uptime').filter(type__contains='动漫')[:12]
    animent_data_list = [{  'id' : i.id,
                        'title':i.title,
                        'state':i.state,
                        'type':eval(i.type)[0],
                        'cover':i.cover,} for i in animent_data]
    DataDic = {
        'code':200,
        'all_data':all_data_list,
        'china_data':china_data_list,
        'europe_data':europe_data_list,
        'hong_kong_data':hong_kong_data_list,
        'chine_zy_data_list':chine_zy_data_list,
        'animent_data_list':animent_data_list,
    }
    return JsonResponse(DataDic)


# 获取动漫详细信息
def GetDetail(request):
    AnimentId = request.GET.get('id')
    AnimentData = Animent_table.objects.get(id=AnimentId)
    AnimentData.click_nub +=1
    AnimentData.save()
    VideoPage = eval(AnimentData.video_url_list)
    VideoPage = [i['page'] for i in VideoPage]
    class_data = Animent_table.objects.order_by('-uptime').filter(type__contains=eval(AnimentData.type)[0])[:8]
    class_data = [{'id': i.id,
                    'title': i.title,
                    'state': i.state,
                    'type': eval(i.type)[0],
                    'cover': i.cover,} for i in class_data]
    HotData = Animent_table.objects.order_by('-click_nub')[:6]
    HotDataList = [{
        'id': i.id,
        'title': i.title,
        'state': i.state,
        'type': eval(i.type)[0],
        'cover': i.cover,
        'yere': str(i.uptime)[:4],
    } for i in HotData]
    DataDic = {
        'code':200,
        'data': {
            'id': AnimentData.id,
            'title': AnimentData.title,
            'state': AnimentData.state,
            'type': eval(AnimentData.type)[0],
            'cover': AnimentData.cover,
            'author': AnimentData.author,
            'synopsis': AnimentData.synopsis,
            'cartoon_voice': AnimentData.cartoon_voice,
            'uptime':AnimentData.uptime.strftime("%Y-%m-%d %H:%M:%S"),
            'score':AnimentData.score,
            'VideoPage': VideoPage,
        },
        'HotDataList':HotDataList,
        'classAniment': class_data
    }

    return JsonResponse(DataDic)

# 获取评分
class AnimentGetScore(APIView):
    def get(self, request):
        AnimentId = request.GET.get('AnimentId')
        token = request.headers
        token = token['Token']
        userToken = UserToken.objects.get(token=token)
        user = userToken.user
        userScoreDic = eval(user.user_score_dic)
        if str(AnimentId) in userScoreDic:
            score = userScoreDic[str(AnimentId)]
            return JsonResponse({'code':201, 'score':score})
        else:
            return JsonResponse({'code': 201, 'score': 0})


# 动画评分
class AnimentSetScore(APIView):
    def get(self, request):
        Score = request.GET.get('score')
        AnimentId = int(request.GET.get('AnimentId'))
        token = request.headers
        token = token['Token']
        userToken = UserToken.objects.get(token=token)
        user = userToken.user
        userScoreDic = eval(user.user_score_dic)
        if str(AnimentId) in userScoreDic:
            return JsonResponse({'msg': '已经评分过了', 'code':401, 'score':userScoreDic[str(AnimentId)]},status=401)
        userScoreDic[str(AnimentId)] = Score
        user.user_score_dic = userScoreDic

        Animent = Animent_table.objects.get(id=AnimentId)
        if Animent.score == 0:
            Animent.score = float(Score)
        else:
            Animent.score = (Animent.score+float(Score)) / 2
        user.save()
        Animent.save()
        return JsonResponse({'msg': '评分成功', 'code':201},status=201)


def GetVideo(request):
    AnimentPage = request.GET.get('page')
    AnimentId = request.GET.get('id')
    AnimentData = Animent_table.objects.get(id=AnimentId)
    VideoData = eval(AnimentData.video_url_list)
    VideoPage = [i['page'] for i in VideoData]

    # 相关推荐
    class_data = Animent_table.objects.order_by('-uptime').filter(type__contains=eval(AnimentData.type)[0])[:8]
    class_data = [{'id': i.id,
                    'title': i.title,
                    'state': i.state,
                    'type': eval(i.type)[0],
                    'cover': i.cover,} for i in class_data]
    dicData = {}
    for i in VideoData:
        if str(AnimentPage) == str(i['page']):
            newtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            urldata = {'data':i['url'],
                       'time':newtime}

            dicData['viveoUel'] = i['url']
            break
    # print(dicData['viveoUel'])
    dicData['Title'] = AnimentData.title
    dicData['cover'] = AnimentData.cover
    dicData['synopsis'] = AnimentData.synopsis
    dicData['ClassAniment'] = class_data
    dicData['VideoPage'] = VideoPage
    dicData['id'] = AnimentData.id
    return JsonResponse(dicData)

def GetKindsAniment(request):
    kind = request.GET.get('kind')

    channel = request.GET.get('channel')
    area = request.GET.get('area')
    if channel=="电视剧":
        channel = '剧'
    page = request.GET.get('page') if request.GET.get('page') else 1
    number = request.GET.get('number') if request.GET.get('number') else 36
    if (not kind or kind == '全部') and (not channel or channel =='全部') and (not area or area == '全部'):
        AnimentData = Animent_table.objects.order_by('-uptime')

    elif (kind and kind != '全部') and (not channel or channel =='全部') and (not area or area == '全部'):
        AnimentData = Animent_table.objects.order_by('-uptime').filter(type__contains=kind)

    elif (kind and kind != '全部') and (channel and channel !='全部') and (not area or area == '全部'):
        AnimentData = Animent_table.objects.order_by('-uptime').filter(Q(type__contains=kind), Q(type__contains=channel))

    elif (kind and kind != '全部') and (channel and channel !='全部') and (area and area != '全部'):
        AnimentData = Animent_table.objects.order_by('-uptime').filter(Q(type__contains=kind), Q(type__contains=channel), Q(type__contains=area))

    elif (kind and kind != '全部') and (not channel or channel =='全部') and (area and area != '全部'):
        AnimentData = Animent_table.objects.order_by('-uptime').filter(Q(type__contains=kind), Q(type__contains=area))

    elif (not kind or kind == '全部') and (channel and channel !='全部') and (not area or area == '全部'):
        AnimentData = Animent_table.objects.order_by('-uptime').filter(type__contains=channel)
        
    elif (not kind or kind == '全部') and (channel and channel !='全部') and (area and area != '全部'):
        AnimentData = Animent_table.objects.order_by('-uptime').filter(Q(type__contains=channel), Q(type__contains=area))

    elif (not kind or kind == '全部') and (not channel or channel =='全部') and (area and area != '全部'):
        AnimentData = Animent_table.objects.order_by('-uptime').filter(type__contains=area)
    total = len(AnimentData)
    AnimentData = Paginator(AnimentData, number)
    pageNumber = AnimentData.num_pages
    AnimentData = AnimentData.page(page)

    AnimentList = [{'id': i.id,
                    'title': i.title,
                    'state': i.state,
                    'type': eval(i.type)[0],
                    'cover': i.cover,
                    'synopsis': i.synopsis} for i in AnimentData]

    return JsonResponse({'code':200,'AnimentData':AnimentList,'pageNumber': pageNumber, 'total': total})

def SearchAniment(request):
    searchData = request.GET.get('search')
    page = request.GET.get('page') if request.GET.get('page') else 1
    number = request.GET.get('number') if request.GET.get('number') else 36
    AnimentData = Animent_table.objects.filter(title__contains=searchData)
    AnimentData = Paginator(AnimentData, number)
    pageNumber = AnimentData.num_pages
    AnimentData = AnimentData.page(page)

    AnimentList = [{'id': i.id,
                    'title': i.title,
                    'state': i.state,
                    'type': eval(i.type)[0],
                    'author': i.author,
                    'cover': i.cover,
                    'yere':str(i.uptime)[:4],
                    'synopsis': i.synopsis} for i in AnimentData]

    HotData = Animent_table.objects.order_by('-click_nub')[:6]
    HotDataList = [{
        'id': i.id,
        'title': i.title,
        'state': i.state,
        'type': eval(i.type)[0],
        'cover': i.cover,
        'yere': str(i.uptime)[:4],
    } for i in HotData]

    return JsonResponse({'code':200,'AnimentData':AnimentList,'HotDataList':HotDataList,'pageNumber': pageNumber})

class AnimentMessage(APIView):
    def post(self, request):
        message = json.loads(request.body)
        message = message['message']
        cheakRe = '^.*(?=.*[@$%^&*_+?><:"])[@$%^&*_+?><:"|/=-]{1,}$'
        if re.findall(cheakRe, message) or not message:
            return JsonResponse({'code': 401, 'msg': '发送内容错误,不能为空和有部分特殊字符'},status=401)
        token = request.headers
        token = token['Token']
        userToken = UserToken.objects.get(token=token)
        user = userToken.user
        newtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        messageDb = leave_word(
            ursename=user.user_name,
            content=message,
            urse_img=user.user_cover,
            time=newtime,
            reply='[]'
        )
        messageDb.save()
        messageDb.up_user_message.add(user)
        return JsonResponse({'code': 200, 'msg': '添加成功'})

def GetAnimentMessage(request):
    page = request.GET.get('page') if request.GET.get('page') else 1

    number = request.GET.get('number') if request.GET.get('number') else 24
    MessageList = leave_word.objects.all().order_by('-time')
    MessageList = Paginator(MessageList, number)
    TotalPageList = MessageList.num_pages
    MessageList = MessageList.page(page)

    ReturnMessageList = [{
        'id': i.id,
        'userName': (i.up_user_message.get()).user_name,
        'message': i.content,
        'reply': eval(i.reply) if i.reply else i.reply,
        'urseImg': i.up_user_message.get().user_cover,
        'sentTime':i.time.strftime("%Y-%m-%d %H:%M:%S")
    } for i in MessageList]

    dic = {
        'code': 200,
        'TotalPageList': TotalPageList,
        'MessageList': ReturnMessageList
    }
    return JsonResponse(dic)
# 留言回复格式{'userid':4,'userName':'cwy','time':'2023-07-55','message':'test'}


class AnimentCollection(APIView):
    '''视频收藏'''
    # post 请求
    def post(self, request):
        # 获取参数
        Animent_id = json.loads(request.body)
        Animent_id = Animent_id['Animent_id']
        # 查询用户
        user = users_table.objects.get(user_name=self.request.user)
        AnimentData = Animent_table.objects.get(id=Animent_id)
        # 添加收藏
        user.user_like_animent.add(AnimentData)
        return JsonResponse({'code': 200, 'msg': '收藏成功'})
    # get请求
    def get(self, request):
        token = request.headers
        token = token['Token']
        userToken = UserToken.objects.get(token=token)
        user = userToken.user
        like_Animent = user.user_like_animent.all()

        like_Animent_list = [
            {'id': i.id,
             'title': i.title,
             'state': i.state,
             'type': eval(i.type)[0],
             'author': i.author,
             'cover': i.cover,
             }
        for i in like_Animent]
        return JsonResponse({'code':200, 'CollectionAniment': like_Animent_list})

    def delete(self, request):
        Animent_id = request.GET.get('Animent_id')
        token = request.headers
        token = token['Token']
        userToken = UserToken.objects.get(token=token)
        user = userToken.user
        Aniemnt = user.user_like_animent.get(id=Animent_id)
        user.user_like_animent.remove(Aniemnt)
        return JsonResponse({'code': 200, 'msg': '取消成功'})