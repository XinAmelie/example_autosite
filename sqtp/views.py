from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from httprunner.cli import main_run  # hrun命令行相关的处理
from rest_framework.decorators import api_view, authentication_classes, permission_classes,action  # ，函数视图装饰器 @api_view
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.parsers import JSONParser # 反序列化
from rest_framework.permissions import IsAuthenticated #是否登录
from sqtp.models import Request,Case,Step,Project,Environment,User
from sqtp.permissions import IsOwnerOrReadOnly
from sqtp.serializers import RequestSerializer,CaseSerializer,StepSerializer,ProjectSerializer,EnvironmentSerializer,\
    UserSerializer,RegisterSerializer,LoginSerializer

from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth # django内置的模块,处理用户相关的

import subprocess  #命令行模块


###################################################视图################################################################

# # get查询 post新增 put修改 delete删除
# @api_view(['GET','POST']) # 列表中中是允许的请求方法
# def request_list(request,format=None):
#     # 一个视图可以有多个处理动作actions
#
#     if request.method == 'GET': # 处理查询的请求
#         # 针对当前数据模型的所有数据
#         serializer = RequestSerializer(Request.objects.all(),many=True)
#         print(serializer.data) # 因为序列化后的数据都是放在data中的
#         print(request.data)
#         # 返回json格式响应
#         # return JsonResponse(data=serializer.data,safe=False) #safe=False是为了支持字典以外的python对象转化成json
#         return Response(serializer.data) # 自动分配返回的对象
#     elif request.method=='POST': # 处理新增的请求   # elif 就是当走到符合查询条件的语句后，后面所有的elif和else就不会再被执行；
#         # rf框架独有的request.data可以把数据转换为python的基础类型
#
#         # 如果RequestSerializer中的第一参数未传，就是新增数据json
#         serializer=RequestSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#
# # json是一个序列化数据  dataobject是反序列化的数据
# @api_view(['GET','PUT','DELETE'])
# def request_detail(request,_id,format=None): # format=None路由传过来的格式化的名称
#     try:
#         req_obj = Request.objects.get(id=_id)
#         print(req_obj)
#         # 序列化
#         # serializer=RequestSerializer(req_obj)
#         # return Response(serializer.data)
#     except Exception:
#         return Response(status=status.HTTP_404_NOT_FOUND) # 返回错误的状态码
#     if request.method=='GET':
#         serializer = RequestSerializer(req_obj)
#         return Response(serializer.data)
#     elif request.method == 'PUT':  #修改,采用序列化器
#         # data=request.data待序列化的数据
#         # req_obj如果第一个参数传递了，就会用data覆盖掉req_obj
#         serializer = RequestSerializer(req_obj,data=request.data)
#         if serializer.is_valid(): # 判断data中的数据是否符合要求
#             serializer.save()
#             return Response(serializer.data,status =status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE': # 删除
#         req_obj.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)



############################################ 类视图 ############################################################

# from rest_framework.views import APIView

# class Requestlist(APIView):
#     '''覆盖了查询和详情的功能'''
#     def get(self,request,format=None):
#         # 针对当前数据模型的所有数据
#         serializer = RequestSerializer(Request.objects.all(),many=True)
#         print(serializer.data) # 因为序列化后的数据都是放在data中的
#         print(request.data)
#         # 返回json格式响应
#         # return JsonResponse(data=serializer.data,safe=False) #safe=False是为了支持字典以外的python对象转化成json
#         return Response(serializer.data) # 自动分配返回的对象
#     def post(self,request,format=None):
#         # 处理新增的请求   # elif 就是当走到符合查询条件的语句后，后面所有的elif和else就不会再被执行；
#         # rf框架独有的request.data可以把数据转换为python的基础类型
#         # 如果RequestSerializer中的第一参数未传，就是新增数据json
#         serializer=RequestSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# # 改写request_detail视图方法
# class ReauestDetail(APIView):
#     '''覆盖父类get_object方法实现'''
#     # url传的id可以不用，但是必须接收
#     def get_object(self,_id,format=None):
#         try:
#             req_obj = Request.objects.get(id=_id)
#             return req_obj
#         except Exception:
#             return Response({"error":"data not found"},status=status.HTTP_404_NOT_FOUND)  # 返回错误的状态码
#
#     def get(self,request,_id,format=None):
#         req_obj=self.get_object(_id)
#         # 如果是异常的响应
#         # isinstance类型判断
#         if isinstance(req_obj,Response):
#             return req_obj
#
#         serializer = RequestSerializer(req_obj)
#         return Response(serializer.data)
#     def put(self,request,_id,format=None):
#         req_obj = self.get_object(_id)
#         # isinstance类型判断
#         if isinstance(req_obj, Response):
#             return req_obj
#         serializer = RequestSerializer(req_obj, data=request.data)
#         if serializer.is_valid():  # 判断data中的数据是否符合要求
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,_id,format=None):
#         req_obj = self.get_object(_id)
#         # isinstance类型判断
#         if isinstance(req_obj, Response):
#             return req_obj
#         req_obj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# 代码再优化，草你吗的，不直接写出来

##############################################通用类视图####################################################
# ListCreateAPIView查询所有和创建
# RetrieveUpdateDestroyAPIView 针对单个数据修改删除查
# from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
#
# class Requestlist(ListCreateAPIView):
#     '''
#     查询所有的数据和新增单个数据的功能
#     '''
#     queryset = Request.objects.all() # 数据的查询集
#     serializer_class=RequestSerializer #  # 把序列化类告诉他
#
# class ReauestDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Request.objects.all()  # 数据的查询集
#     serializer_class = RequestSerializer # 把序列化类告诉他




# from rest_framework import viewsets
# from drf_yasg.utils import swagger_auto_schema
# from django.utils.decorators import method_decorator
#
#
# ###############################################视图集#####################################################
# # 优化3：视图集--增删改查   定制化的注释
# # name都是固定的
# @method_decorator(name='list',decorator=swagger_auto_schema(operation_summary='列出所有数据',operation_description='列出请求的数据.....'))
# @method_decorator(name='create',decorator=swagger_auto_schema(operation_summary='创建数据',operation_description='增加请求的数据.....'))
# @method_decorator(name='retrieve',decorator=swagger_auto_schema(operation_summary='查看单个数据',operation_description='查看单个请求的数据.....'))
# @method_decorator(name='destroy',decorator=swagger_auto_schema(operation_summary='删除请求的数据',operation_description='删除数据.....'))
# @method_decorator(name='update',decorator=swagger_auto_schema(operation_summary='更新请求的数据',operation_description='更新数据.....'))
# class RequestViewSet(viewsets.ModelViewSet):
#     queryset = Request.objects.all()  # 数据的查询集
#     serializer_class = RequestSerializer
#
# class CaseViewSet(viewsets.ModelViewSet):
#     queryset = Case.objects.all()
#     serializer_class = CaseSerializer
#
#     # 同步创建用户 钩子函数会自动的调用
#     def perform_create(self, serializer):
#         serializer.save(create_by=self.request.user)
#     # 同步更新用户 钩子函数会自动的调用
#     def perform_update(self, serializer):
#         serializer.save(updated_by=self.request.user)
#
#     # 自定义一个请求参数
#     @action(methods=['GET'],detail=True,url_path='run',url_name='run_case')
#     # 完整的url 等于/cases/<int:case_id>/run
#     def run_case(self,request,pk):  #视图函数，接收请求和接收pk
#         # 获取序列化器
#         case = Case.objects.get(pk=pk) #根据id获取当前的用例
#         serialzier = self.get_serializer(instance = case)
#         path = serialzier.to_json_file()
#
#         # 执行用例，也就是利用hrun XX.json 命令行，但是有缺点，无法展示输出的结果
#         # subprocess.Popen(f'hrun {path}',shell=True)
#
#         # HR3 API的执行方法
#
#         # 根据退出代码判断是否执行成功
#         exit_code = main_run([path])
#         main_run([path])
#         if exit_code != 0:
#             return Response(data={'error': 'failed run case', 'retcode': exit_code},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         return Response(data={'msg': 'run success', 'retcode': 200})
#
#
# class StepViewSet(viewsets.ModelViewSet):
#     '''用例步骤'''
#     queryset = Step.objects.all()
#     serializer_class = StepSerializer

# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     # 因为用的是视图集，所以加权限即可，实现局部的作用。  视图函数用装饰器；视图集直接加即可
#
#     '''
#     authentication_classes = ((BasicAuthentication,SessionAuthentication))
#     permission_classes = ((IsAuthenticated,))
#     这个是搭配的。
#     '''
#     # 局部认证。我现在想禁用
#     authentication_classes = ((BasicAuthentication,SessionAuthentication))
#     permission_classes = ((IsAuthenticated,IsOwnerOrReadOnly))  # IsOwnerOrReadOnly是定义的权限
#
#
# class EnvironmentViewSet(viewsets.ModelViewSet):
#     queryset = Environment.objects.all()
#     serializer_class = EnvironmentSerializer
#
#     # 局部认证。我现在想禁用全局认证  。只需要把元组设置为空的即可
#     # authentication_classes = ()
#     permission_classes = (())    # 检查令牌是空的




# @api_view(['GET'])
# # @login_required   # 装饰器 校验用户是否登录 防止用户在接口层登录
# # 利用rf的装饰器
# # 视图函数现在想禁用全局认证，直接设置为空即可
# @authentication_classes((BasicAuthentication,SessionAuthentication))
# # 想要BasicAuthentication，SessionAuthentication生效需要加权限类的装饰器
# @permission_classes((IsAuthenticated,))
# # 放在具体的视图，就是局部的使用，即只有这个视图函数去这样处理身份和权限的认证
#
# def user_list(request):
#     query_set = User.objects.all()
#     serializer = UserSerializer(instance=query_set,many=True)
#     return Response(serializer.data)
#
#
#
#
# '''
# 1）用于序列化时，将模型类对象传入instance参数
#
# 2）用于反序列化时，将要被反序列化的数据传入data参数
#
# 3）除了instance和data参数外，在构造Serializer对象时，还可通过context参数额外添加数据，如
#
# serializer = StudentSerializer(student, context={'request': request},many=False)
#
# '''
#
#
# @api_view(['GET'])
# def user_detail(request,_id):
#     try:
#         # pk就是primary key主键
#         user = User.objects.get(pk=_id)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     serializer = UserSerializer(instance=User)
#     return Response(serializer.data)
#
#
# # 注册视图
# @api_view(['POST'])
# @permission_classes(())  #该接口解除全局认证和全局权限
# def register(request):
#     # 获取序列化器
#     serializer=RegisterSerializer(data=request.data)
#     if serializer.is_valid(): #根据序列器和模型字段综合检查数据是否合法
#         user = serializer.register() # 创建用户
#         auth.login(request,user) # 完成用户登录状态设置
#         return Response(data={'msg':'register','is_admin':user.is_superuser,'retcode':status.HTTP_201_CREATED},status=status.HTTP_201_CREATED)
#     return Response(data={'msg':'error','retcode':status.HTTP_400_BAD_REQUEST,'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
#
#
#
# # 登录视图 rf框架不论什么请求都是request.data
# @api_view(['POST'])
# @permission_classes(()) #该接口解除全局认证和全局权限
# def login(request):
#     # 获取登录信息 --序列器
#     serializer=LoginSerializer(data=request.data)
#     user = serializer.validate(request.data)
#     if user:
#         auth.login(request, user)  # 登录存储session信息
#         return Response(data={'msg': 'login success', 'to': 'index.html'}, status=status.HTTP_302_FOUND)
#     return Response(data={'msg': 'error', 'retcode': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors},
#                     status=status.HTTP_400_BAD_REQUEST)
#
#
# # 登出视图
# @api_view(['GET'])
# def logout(request):
#     # 可以rf框架直接获取
#     # is_authenticated采用了django的auth系统
#     if request.user.is_authenticated: # 判断用户是否是登录的状态，此时利于的是django的能力，不是rf框架
#         auth.logout(request) #登出，清除session
#     return Response(data={'msg':'logout success','to':'login.html'},status=status.HTTP_302_FOUND)
#
#
# # 禁用认证。像注册和登录 以及查询当前的用户接口是不需要校验的
#
# #当前用户信息
# @api_view(['GET'])
# @permission_classes(()) #该接口解除全局认证和全局权限
# def current_user(request):
#     if request.user.is_authenticated: #如果当前用户处于登录状态
#         # 返回当前用户信息
#         serializer = UserSerializer(request.user)
#         return Response(data=serializer.data)
#     else:
#         return Response(data={'retcode': 403, 'msg': '未登录', 'to': 'login.html'}, status=403)













# @swagger_auto_schema(method='GET',operation_summary='用户定制化接口摘要信息',operation_description='用户定制化接口描述信息....')
# @api_view(['GET'])
# # 用户定制的接口
# def customer_api(request):
#     return Response(data={"retcode":status.HTTP_200_OK,"msg":"testing..."})


