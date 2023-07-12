# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/5 0:10
Author : 王新科
File : hr3.py
software : PyCharm
============================
"""

from django.db import models
from .mgr import Project

from .base import CommonInfo
# Create your models here.

# 核心models
class Config(CommonInfo):
    project=models.ForeignKey(Project,on_delete=models.DO_NOTHING,null=True) #非必填写
    name = models.CharField(verbose_name='名称',max_length=128) # verbose_name是别名字 verbose_name可省略
    base_url = models.CharField(verbose_name='IP/域名',max_length=256,null=True,blank=True) # 可为空，可空白(就是什么都不填写)
    variables = models.JSONField('变量',null=True) # 不寻常的值，例如键值对 列表 布尔之类的用jsonfileld
    # 通过models.JSONField可指定此字段为存储类型为JSON格式
    parameters = models.JSONField('参数', null=True)
    export = models.JSONField('用例返回值', null=True)
    verify = models.BooleanField('https校验', default=False)


    # 后期序列化需要使用到
    class Meta(CommonInfo.Meta):  # 模型元类的作用，提供些额外的信息，比如模型对应的表名
        # db_table=['Config'] # 如果不设置 默认的名称是app名_模型名
        verbose_name='用例配置' # 或者写pass也可以，反正是继承

class Case(CommonInfo):
    config = models.OneToOneField('Config',on_delete=models.DO_NOTHING) # config被删除了，什么都不做
    file_path = models.CharField('用例文件路径',max_length=1000,default='demo_case.json')

    def __str__(self):
        return self.config.name

    class Meta(CommonInfo.Meta):
        verbose_name='测试用例表'


class Step(CommonInfo):
    # 属于那条用例
    # related_name反向查询名称，同个模型中，两个以上字段关联同一个模型，必须指定related_name
    belong_case = models.ForeignKey(Case,on_delete=models.CASCADE,related_name='teststeps')
    # 引用那个case
    linked_case = models.ForeignKey(Case,on_delete=models.SET_NULL,null=True,related_name='linked_steps')
    name = models.CharField('名称', max_length=128)
    variables = models.JSONField('变量', null=True)
    extract = models.JSONField('请求返回值', null=True)
    validate = models.JSONField('校验项', null=True)
    # 前置后置的操作，只存在步骤级
    setup_hooks = models.JSONField('初始化', null=True)
    teardown_hooks = models.JSONField('清除', null=True)
    sorted_no = models.PositiveSmallIntegerField('步骤顺序',default=1) # PositiveSmallIntegerField正整数



    class Meta(CommonInfo.Meta):
        verbose_name = '测试用例表'
        ordering = ['id','sorted_no']
        # 联合约束 使用这种联合约束，保证数据库能不重复添加用户
        unique_together = ['belong_case','sorted_no'] # # 同一个用例的步骤顺序是不一样的  同一个用例stored_no不可以相同，引用其他的用例。stored_no可以相同



class Request(CommonInfo):
    method_choices = (  # method可选的字段，
        (0, 'GET'),  # 参数1:实际存储在数据库中的值, 参数2：对外显示的值
        (1, 'POST'),
        (2, 'PUT'),
        (3, 'DELETE')
    )
    step = models.OneToOneField(Step,on_delete=models.CASCADE,null=True,related_name='request')
    method = models.SmallIntegerField('请求方法',choices=method_choices,default=0)
    url = models.CharField('请求路径', default='/', max_length=1000)
    params = models.JSONField('url参数', null=True)
    headers = models.JSONField('请求头', null=True)
    cookies = models.JSONField('Cookies', null=True)
    data = models.JSONField('表单参数', null=True)
    json = models.JSONField('json参数', null=True)

    def __str__(self):
        return self.url

    class Meta(CommonInfo.Meta):
        verbose_name = '请求信息表'
