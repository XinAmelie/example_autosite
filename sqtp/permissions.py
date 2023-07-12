# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/12 22:07
Author : 王新科
File : permissions.py
software : PyCharm
============================
"""

from rest_framework import permissions

# 自定义权限类,背景是当前项目的管理员
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        # 如果是访问之类的Http方法，就通过
        if request.method in permissions.SAFE_METHODS:
            return True
        # 否则返回只有该项目管理员才能编辑
        # 即判断当前用户是否是该项目的管理员
        return obj.admin == request.user

