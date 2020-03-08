from django.db import models
from django.utils import timezone


# 基类
class Base(models.Model):
    # 创建时间
    create_time = models.DateTimeField(default=timezone.now,null=True)

    class Meta:
        # 可继承
        abstract = True


# 用户类
class User(Base):

    # 用户名
    username = models.CharField(max_length=200)
    # 密码
    password = models.CharField(max_length=200)
    # 头像
    img = models.CharField(max_length=200)
    # 类别    0--普通用户     1--超级管理员       2--VIP
    type = models.IntegerField()

    # 声明表名
    class Meta:
        db_table = "user"