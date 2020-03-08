from django.shortcuts import render, redirect
# 导包
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
# 导入类视图
from django.views import View

# from myapp.models import User
import json
from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.views import APIView
# 导入加密库
import hashlib
# 导入图片库
# 绘画库
from PIL import ImageDraw
# 字体库
from PIL import ImageFont
# 图片库
from PIL import Image
# 随机库
import random
# 文件流
import io

import requests

# 导入上传文件夹配置
from mydjango.settings import UPLOAD_ROOT
import os

# 导入原生sql模块
from django.db import connection

import jwt

# 导入redis数据库
import redis

# 导入时间模块
import time

# 导入公共目录变量
from mydjango.settings import BASE_DIR

# 导包
from django.db.models import Q, F

# 导入dwebsocket的库
from dwebsocket.decorators import accept_websocket
import uuid

# 导入数据库
from .models import *

# 序列化
from .myser import *

# 导包
import redis

# 定义ip 和端口
host = '127.0.0.1'
port = 6379
# 建立连接
r = redis.Redis(host=host, port=port)


# 定义验证码类
class MyCode(View):
    # 定义随机颜色
    def get_random_color(self):
        R = random.randrange(255)
        G = random.randrange(255)
        B = random.randrange(255)
        return (R, G, B)

    # 试验CMYK
    def cmyk(self):
        C = random.randrange(100)
        M = random.randrange(100)
        Y = random.randrange(100)
        K = random.randrange(100)
        return (C, M, Y, K)

    # 定义获取验证码视图
    def get(self, request):
        # 定义画布
        img_size = (150, 60)
        # 定义图像对象
        image = Image.new('CMYK', img_size, 'white')
        # 定义画笔对象
        draw = ImageDraw.Draw(image, 'CMYK')
        # 定义随机字符串
        source = '0123456789abcdefghijklmnopqrstuvwxyz'
        # 容器
        code_str = ''
        times = random.randrange(3,5)
        for i in range(times):
            # 获取随机颜色
            text_color = self.cmyk()
            # 获取随机字符串下标
            tmp_num = random.randrange(len(source))
            # 获取字符集
            random_str = source[tmp_num]
            # 拼接到容器中
            code_str += random_str
           # 将字符串添加到画布上
            # 定义字体
            ft = ImageFont.truetype(font='C:\\Windows\\Fonts\\Arial.ttf', size=20)

            draw.text((10+30*i, 20), random_str,text_color, font=ft)

        # 存入redis
        r.set('code', code_str)
        # 建立缓存区
        buf = io.BytesIO()
        # 保存图片
        image.save(buf,'jpeg')
        # 带头部信息返回
        return HttpResponse(buf.getvalue(), 'image/jpeg')





# md5加密方法
def make_password(mypass):
    # 生成md5对象
    md5 = hashlib.md5()

    # 定义加密对象
    sign_str = str(mypass)

    # 转码
    sign_utf8 = sign_str.encode(encoding='utf-8')

    # 加密
    md5.update(sign_utf8)

    # 生成秘钥
    md5_server = md5.hexdigest()

    return md5_server


# 注册模块
class Register(APIView):
    def get(self, request):
        # 接收参数
        username = request.GET.get('username', 'null')
        password = request.GET.get('password', ' null')
        code = request.GET.get('code')

        # 获取验证码
        redis_code = r.get('code')
        # 转码
        redis_code = redis_code.decode('utf8')

        res = {}
        if code != redis_code:
            res['code'] = 405
            res['message'] = '验证码错误'
            return Response(res)



        # 排重
        user = User.objects.filter(username=username).first()


        if user:
            res['code'] = 405
            res['message'] = '该用户名已存在'

        else:
            # 入库
            user = User(username=username, password=make_password(password), type=0, img='')

            user.save()

            res['code'] = 200
            res['message'] = '注册成功'

        return Response(res)
