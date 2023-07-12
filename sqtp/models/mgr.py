# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/5 0:16
Author : 王新科
File : mgr.py
software : PyCharm
============================
"""
from django.db import models
from .base import CommonInfo
from django.conf import settings

class Project(CommonInfo):
    # 枚举值
    PRO_STATUS = (
        (0, '开发中'),
        (1, '维护中'),
        (2, '稳定运行'),
    )

    # 字段中2个指定了相同的数据表，所以在反向查询的时候会报错。需要加related_name去标注
    # 管理员
    admin = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.DO_NOTHING,verbose_name='项目管理员',related_name='project_admin')
    # 成员
    # 多对多在哪个模型中设置ManyToManyField并不重要，在两个模型中任选一个即可 ;不要两个模型都设置。
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,verbose_name='项目成员',related_name='project_members')
    # 名称
    name = models.CharField(verbose_name='项目名称',max_length=32,unique=True)
    # 状态
    status = models.SmallIntegerField('项目状态',choices=PRO_STATUS,default=2)
    # 版本
    version = models.CharField('项目版本',max_length=32,default='v0.1')


    # Meta需要设置
    class Meta(CommonInfo.Meta): # # 元类需要显示继承父类的元类才会生效
     # 当子类meta中的字段和父类的meta中的字段重名，就会以子类为准覆盖父类，当父亲中无，子有，会进行正常的拼接。
        verbose_name='项目表' # 适用于模型定义名义抽象的

class Environment(CommonInfo):
    # 服务器类型选项
    service_type = (

        ('0','web服务器'),
        ('1','数据库服务器')

    )
    # 操作系统
    serivce_os = ((0,'windows'),(1,'Linux'))
    # 服务器状态
    service_status = (
        (0, 'active'),
        (1, 'disable')
    )
    project = models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name='所属项目')
    # ip django-ORM 提供genericIPAddressField专门存储ip类型的信息
    ip = models.GenericIPAddressField('IP地址',default='127.0.0.1')
    port = models.PositiveSmallIntegerField(default=80,verbose_name='端口号')    # PositiveSmallIntegerField 正数，无负数
    # 服务器类型
    category = models.SmallIntegerField('服务器类型',choices=service_type,default=0,)
    os = models.SmallIntegerField('服务器操作系统',choices=serivce_os,default=0) # 不想浪费资源所以小整数就行
    status = models.SmallIntegerField('服务器状态',choices=service_status,default=0)
    def __str__(self):
        return self.ip+':'+self.port

    class Meta(CommonInfo.Meta):
        verbose_name='测试环境'
