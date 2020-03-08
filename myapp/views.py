from django.shortcuts import render,redirect
#导包
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,QueryDict
#导入类视图
from django.views import View

#from myapp.models import User
import json
from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.views import APIView
#导入加密库
import hashlib
#导入图片库
#绘画库
from PIL import ImageDraw
#字体库
from PIL import ImageFont
#图片库
from PIL import Image
#随机库
import random
#文件流
import io

import requests

#导入上传文件夹配置
from mydjango.settings import UPLOAD_ROOT
import os

#导入原生sql模块
from django.db import connection

import jwt

#导入redis数据库
import redis

#导入时间模块
import time

#导入公共目录变量
from mydjango.settings import BASE_DIR

#导包
from django.db.models import Q,F

#导入dwebsocket的库
from dwebsocket.decorators import accept_websocket
import uuid

# 导入数据库
from .models import *

# 序列化
from .myser import *


#方法视图
def myindex(request):

    return HttpResponse('1')


# 类视图
class MyView(View):

    greeting = '欢迎'

    def get(self,request):

        user_list = User.objects.all()

        ser = UserSer(user_list,many=True)

        user_list = ser.data

        return render(request, 'index.html', locals())

    def post(self,request):

        # 接收参数
        username = request.POST.get('username')

        password = request.POST.get('password')

        type = request.POST.get('type')
        print(type)

        # 入库
        user = User(username=username, password=password, type=type, img='')

        user.save()

        return redirect('/my_view/')

    def put(self,request):
        # 解析数据
        info = QueryDict(request.body)
        print(info)
        # 接收变量
        id = info.get('id')
        username = info.get('username')
        password = info.get('password')
        type = info.get('type')
        print(id)
        # 修改数据库
        user = User.objects.filter(id=id).first()
        # 查重
        if username and not User.objects.filter(username=username).first():
            user.username = username
        else:
            if not username == User.objects.get(id=id).username:
                print('用户名重复')
        if password:
            user.password = password
        if type:
            user.type = type
        user.save()

        return JsonResponse({'code': 200, 'msg': 'success'}, safe=False)

    def delete(self,request):
        # 解析数据
        info = QueryDict(request.body)

        # 接收目标id
        id = info.get('id')

        # 删除相应数据
        user = User.objects.get(id=id)
        print(user)
        user.delete()

        return JsonResponse({'code': 200, 'msg': 'success'}, safe=False)