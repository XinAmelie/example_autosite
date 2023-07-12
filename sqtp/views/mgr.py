# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/25 23:28
Author : 王新科
File : mgr.py
software : PyCharm
============================
"""


from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated #是否登录
from sqtp.models import Request,Case,Step,Project,Environment,User
from sqtp.permissions import IsOwnerOrReadOnly
from sqtp.serializers import ProjectSerializer,EnvironmentSerializer
from rest_framework import viewsets

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # 因为用的是视图集，所以加权限即可，实现局部的作用。  视图函数用装饰器；视图集直接加即可

    '''
    authentication_classes = ((BasicAuthentication,SessionAuthentication))
    permission_classes = ((IsAuthenticated,))
    这个是搭配的。
    '''
    # 局部认证。我现在想禁用
    authentication_classes = ((BasicAuthentication,SessionAuthentication))
    permission_classes = ((IsAuthenticated,IsOwnerOrReadOnly))  # IsOwnerOrReadOnly是定义的权限


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer

    # 局部认证。我现在想禁用全局认证  。只需要把元组设置为空的即可
    # authentication_classes = ()
    permission_classes = (())    # 检查令牌是空的