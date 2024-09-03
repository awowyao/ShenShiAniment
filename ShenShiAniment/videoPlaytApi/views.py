from django.shortcuts import render
import re
import os
import mimetypes
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
import datetime
from django.http import JsonResponse
# 加密
from ShenShiAniment.settings import videoPlayKey, videoPlayIv
from .aesJiaMi import *
from .rsaJiaMi import *

# 密钥
key = videoPlayKey
iv = videoPlayIv
aes = AEScryptor(key, AES.MODE_CBC, iv, paddingMode="ZeroPadding", characterSet='utf-8')


VideoPath = '/home/diskData/Animents/'
def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data


def stream_video(request):
    """将视频文件以流媒体的方式响应"""
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    # 这里规定存放视频文件夹
    path = str(request.GET.get('path'))
    path = long_decrypt(path)
    rData = str(aes.decryptFromBase64(path))
    rData = eval(rData)
    videotime = datetime.datetime.strptime(str(rData['time']), '%Y-%m-%d %H:%M:%S')
    newtime = datetime.datetime.now()

    timeCha = int((newtime-videotime).total_seconds())
    if timeCha < int(60*60*1.5):
        path = VideoPath + str(rData['data'])
        size = os.path.getsize(path)
        content_type, encoding = mimetypes.guess_type(path)
        content_type = content_type or 'application/octet-stream'
        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte = first_byte + 1024 * 1024 * 15
            if last_byte >= size:
                last_byte = size - 1
            length = last_byte - first_byte + 1
            resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206,
                                         content_type=content_type)
            resp['Content-Length'] = str(length)
            resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        else:
            resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
            resp['Content-Length'] = str(size)
        resp['Accept-Ranges'] = 'bytes'
        return resp
    else:
        return JsonResponse({'code':'0'})