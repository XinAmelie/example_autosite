# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/25 23:20
Author : 王新科
File : __init__.py.py
software : PyCharm
============================
"""


from .auth import user_detail,user_list,current_user,register,logout,login
from .mgr import ProjectViewSet,EnvironmentViewSet
from .hr3 import CaseViewSet,RequestViewSet,StepViewSet,customer_api,FileUploadView
from .task import PlanViewSet,ReportViewSet