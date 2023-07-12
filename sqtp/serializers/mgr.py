# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/13 0:07
Author : 王新科
File : mgr.py
software : PyCharm
============================
"""

from rest_framework import serializers
from sqtp.models import Project,Environment


# 项目
from sqtp.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)  #read_only不作为输入的字段,不校验，但是要用到；不然我创建项目的时候会让我输入create——time字段
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)
    admin_id = serializers.IntegerField(write_only=True)
    admin = UserSerializer(read_only=True) #显示的指定一下
    class Meta:
        model = Project
        fields = ['id', 'admin','admin_id','name', 'status', 'version', 'desc', 'create_time','update_time',] # 指定序列化模型中的字段
        # fields = '__all__'

# 环境
class EnvironmentSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)
    project = ProjectSerializer(read_only=True)
    category = serializers.SerializerMethodField()
    os = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()


    #     # 对于每个具有choices 的字段，每个对象将具有一个get_xx_display() 方法，其中xx 为该字段的名称。 这个方法返回该字段对“人类可读”的值。
    def get_category(self,obj):
        return obj.get_category_display()

    def get_status(self,obj):
        return obj.get_status_display()

    def get_os(self,obj):
        return obj.get_os_display()

    def validate(self, attrs): # 综合校验器
        return attrs

    def validate_project_id(self,project_id): # 单个字段校验器
        # 根据project_id能找到对应的项目

       # count()计数，如果不存在会 ==0，也就是不存在
        # Project模型类中，主键就是project_id
        if not Project.objects.filter(pk=project_id).count():
            raise serializers.ValidationError('请传递正确的project_id')
        return project_id

    class Meta:
        model = Environment
        fields = '__all__'