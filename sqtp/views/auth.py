# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/25 23:21
Author : 王新科
File : auth.py
software : PyCharm
============================
"""


from rest_framework.decorators import api_view, authentication_classes, permission_classes,action  # ，函数视图装饰器 @api_view
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated #是否登录
from sqtp.models import User
from sqtp.serializers import UserSerializer,RegisterSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth # django内置的模块,处理用户相关的


@api_view(['GET'])
# @login_required   # 装饰器 校验用户是否登录 防止用户在接口层登录
# 利用rf的装饰器
# 视图函数现在想禁用全局认证，直接设置为空即可
@authentication_classes((BasicAuthentication,SessionAuthentication))
# 想要BasicAuthentication，SessionAuthentication生效需要加权限类的装饰器
@permission_classes((IsAuthenticated,))
# 放在具体的视图，就是局部的使用，即只有这个视图函数去这样处理身份和权限的认证

def user_list(request):
    query_set = User.objects.all()
    print(query_set)
    serializer = UserSerializer(instance=query_set,many=True)
    return Response(serializer.data)




'''
1）用于序列化时，将模型类对象传入instance参数

2）用于反序列化时，将要被反序列化的数据传入data参数

3）除了instance和data参数外，在构造Serializer对象时，还可通过context参数额外添加数据，如

serializer = StudentSerializer(student, context={'request': request},many=False)

'''


@api_view(['GET'])
def user_detail(request,_id):
    try:
        # pk就是primary key主键
        user = User.objects.get(pk=_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(instance=User)
    return Response(serializer.data)


# 注册视图
@api_view(['POST'])
@permission_classes(())  #该接口解除全局认证和全局权限
def register(request):
    # 获取序列化器
    serializer=RegisterSerializer(data=request.data)
    if serializer.is_valid(): #根据序列器和模型字段综合检查数据是否合法
        user = serializer.register() # 创建用户
        auth.login(request,user) # 完成用户登录状态设置
        return Response(data={'msg':'register','is_admin':user.is_superuser,'retcode':status.HTTP_201_CREATED},status=status.HTTP_201_CREATED)
    return Response(data={'msg':'error','retcode':status.HTTP_400_BAD_REQUEST,'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)



# 登录视图 rf框架不论什么请求都是request.data
@api_view(['POST'])
@permission_classes(()) #该接口解除全局认证和全局权限
def login(request):
    # 获取登录信息 --序列器
    serializer=LoginSerializer(data=request.data)
    user = serializer.validate(request.data)
    if user:
        auth.login(request, user)  # 登录存储session信息
        return Response(data={'msg': 'login success', 'to': 'index.html'}, status=status.HTTP_302_FOUND)
    print(serializer.errors)
    return Response(data={'msg': 'error', 'retcode': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)


# 登出视图
@api_view(['GET'])
def logout(request):
    # 可以rf框架直接获取
    # is_authenticated采用了django的auth系统
    if request.user.is_authenticated: # 判断用户是否是登录的状态，此时利于的是django的能力，不是rf框架
        auth.logout(request) #登出，清除session
    return Response(data={'msg':'logout success','to':'login.html'},status=status.HTTP_302_FOUND)


# 禁用认证。像注册和登录 以及查询当前的用户接口是不需要校验的

#当前用户信息
@api_view(['GET'])
@permission_classes(()) #该接口解除全局认证和全局权限
def current_user(request):
    if request.user.is_authenticated: #如果当前用户处于登录状态
        # 返回当前用户信息
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data)
    else:
        return Response(data={'retcode': 403, 'msg': '未登录', 'to': 'login.html'}, status=403)




