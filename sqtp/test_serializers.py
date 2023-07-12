# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/3 19:16
Author : 王新科
File : test_serializers.py
software : PyCharm
============================
"""

from django.test import TestCase
from sqtp.models import Step,Request
from sqtp.serializers import RequestSerializer # 序列化类
from rest_framework.renderers import JSONRenderer    # JSONRenderer序列化器
from rest_framework.parsers import JSONParser  # 反序列化


# json是一个序列化数据  dataobject是反序列化的数据
class TestRequestSerializer(TestCase):
    '''单元测试'''
    req1 = Request.objects.create(method=1, url='/mgr/teacher1/', data={"name": "小刚", "age": 18, "address": "beijing"})
    print(req1)
    # # 序列化1：数据对象转化成python原生数据类型
    req1_serializer = RequestSerializer(req1)
    print(req1_serializer.data)  # 序列化后的数据存储于序列化对象的data属性中

    # 序列化2,python原生数据类型转化为json
    content = JSONRenderer().render(req1_serializer.data)
    print(content)

    b'{"step":null,"method":1,"url":"/mgr/teacher1/","params":null,"headers":null,"cookies":null,"data":{"name":"\xe5\xb0\x8f\xe5\x88\x9a","age":18,"address":"beijing"},"json":null}'

    # 前端一般传递的数据就是json格式的数据


    # 前端传递的数据，进行反序列化
    # 反序列化1： 将数据流解析为Python原生数据类型   input output数据流

    import io
    steam = io.BytesIO(content)  # 构建一个steam流
    data = JSONParser().parse(steam) #将steam,转化成python原生数据类型  ，steam必须是json的格式
    print("################## steam ########################")
    print(data)

    # 反序列化2:python原生数据转化成模型对象实例
    # 需要数据源
    serializer = RequestSerializer(data=data)
    if serializer.is_valid(): # 校验入参是否合法
        print(serializer.validated_data) # 校验后的的数据
        serializer.save()  # 保存数据对象


    # 序列化器查看结果集,返回完整结果集
    # 序列化多条，需要传many=True
    serializer=RequestSerializer(Request.objects.all(),many=True)
    print(serializer.data)


    # 序列化器内部源码
    print(repr(serializer))






