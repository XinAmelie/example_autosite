# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/13 0:08
Author : 王新科
File : auth.py
software : PyCharm
============================
"""

from rest_framework import serializers
from sqtp.models import User
from rest_framework.exceptions import ValidationError
from django.contrib import auth



from django.conf import settings
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'   # __all__全部校验
        fields = ['date_joined', 'email', 'id', 'is_active', 'is_superuser', 'phone', 'realname', 'username','user_type']


# 注册序列化器
class RegisterSerializer(serializers.ModelSerializer):
    # 因为数据库没有admin_code,所以我们要显性的校验。就是声明一个
    admin_code = serializers.CharField(default='')
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone', 'realname', 'admin_code'] # 选择性的进行校验

    # 手写校验器，入参是否合法;自定义校验规则    is_valid（）是序列化器自带的校验
    def validate(self, attrs): # attrs为入参数的字典形式。是序列化器进行序列化之后的值，被转化为字典
        # 检验admin_code是否正确
        # get方法
        #	key: 要设置默认值的Key
        #	default: 要返回key的值，可以是任何值，如整形、字符串、列表、字典等
        #	return: 如果字典中key本来有值，那么返回的是字典中Key所对应的值，如果没有，那么返回“default”中的值。
        # 程序走到这里发现，get的结果什么都没有。就代表不执行
        if attrs.get('admin_code') and attrs['admin_code'] !='sqtp':
            raise ValidationError('错误的admin code')
        return attrs # 返回校验之后的入参，我后期需要新建数据

    # 注册用户，相当于创建用户数据,我把他写到序列器中了。无所谓
    def register(self):
        # 获取入参数 此时的data是rf框架 data 代表校验之后的数据_validated_dat，框架会自己传attrs
        in_param = self.data
        if 'admin_code' in in_param: # 创建管理员
            in_param.pop('admin_code') # 用户表无admin_code的字段，硬传会报错
            user=User.objects.create_superuser(**in_param)  # 继承的是AbstractUser，父类有方法创建
        else:
            user=User.objects.create_user(**in_param) # 创建普通
        return user

# 登录序列化器
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        # 验证用户名和密码
        user = auth.authenticate(**attrs)
        if not user:
            raise ValidationError('用户名或密码错误')   # ValidationError报的错误会储存在serializer.errors中
        return user #已有的数据