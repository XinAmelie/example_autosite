# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/5 0:38
Author : 王新科
File : base.py
software : PyCharm
============================
"""

# 存放公共的模型

from django.db import models
from django.conf import settings

class CommonInfo(models.Model):
    # 公共字段部分 -- 创建时间，更新时间,描述,创建者和更新者

    create_time = models.DateTimeField('创建时间',auto_now_add=True,null=True) # auto_now_add，只有新增加的时候，才记录
    update_time = models.DateTimeField('更新时间',auto_now=True,null=True) # auto_now生效多次，每次都会记录
    desc = models.TextField(null=True,blank=True,verbose_name='描述')

    # django中反向查询的字段不能是一样的。由于子类继承的时候原封不动的继承，会导致其他的子类出现相同的字段。所以报错
    # 解决办法  %(class)s自动的拼接 例如 step_create_by
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='创建者',on_delete=models.DO_NOTHING,null=True,related_name='%(class)s_create_by')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='更新者',on_delete=models.DO_NOTHING,null=True,related_name='%(class)s_updated_by')

    # 模型类对外暴露的字段

    def __str__(self):
        # 判断当前的数据对象是否有name的属性
        if hasattr(self,'name'):  # hasattr(self,'name') python中反射的一种用法
            return self.name
        else:
            return self.desc    # 返回描述的信息

    # 字段想继承，但是表不想被创建
    # 抽象基类的Meta数据
    class Meta:
        abstract = True # # 当前类为抽象表，字段会被子模型类继承，但是不会创建数据库表 只有abstract这个字段不会被继承
        ordering = ["id"] # 根据id排序 ['-id', ] 倒序