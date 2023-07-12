# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/5 1:24
Author : 王新科
File : auth.py
software : PyCharm
============================
"""
# 用户管理相关的 django内置的User模型
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_type = (
        (0, '开发'),
        (1, '测试'),
        (2, '运维'),
        (3, '项目经理')
    )

    # 真实姓名
    realname = models.CharField('真实姓名',max_length=32)
    phone = models.CharField('手机号',max_length=11,unique=True,null=True,blank=True)
    user_type = models.SmallIntegerField('用户类型',choices=user_type,default=0)

