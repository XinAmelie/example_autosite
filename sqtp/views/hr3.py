# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/25 23:24
Author : 王新科
File : hr3.py
software : PyCharm
============================
"""
import os

from httprunner.cli import main_run
from rest_framework.decorators import api_view, authentication_classes, permission_classes,action  # ，函数视图装饰器 @api_view
from sqtp.models import Request,Case,Step
from sqtp.serializers import RequestSerializer,CaseSerializer,StepSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from httprunner import loader,compat
from rest_framework import serializers

###############################################视图集#####################################################
# 优化3：视图集--增删改查   定制化的注释
# name都是固定的
@method_decorator(name='list',decorator=swagger_auto_schema(operation_summary='列出所有数据',operation_description='列出请求的数据.....'))
@method_decorator(name='create',decorator=swagger_auto_schema(operation_summary='创建数据',operation_description='增加请求的数据.....'))
@method_decorator(name='retrieve',decorator=swagger_auto_schema(operation_summary='查看单个数据',operation_description='查看单个请求的数据.....'))
@method_decorator(name='destroy',decorator=swagger_auto_schema(operation_summary='删除请求的数据',operation_description='删除数据.....'))
@method_decorator(name='update',decorator=swagger_auto_schema(operation_summary='更新请求的数据',operation_description='更新数据.....'))
class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()  # 数据的查询集
    serializer_class = RequestSerializer

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    # 同步创建用户 钩子函数会自动的调用
    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)
    # 同步更新用户 钩子函数会自动的调用
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    # 自定义一个请求参数
    @action(methods=['GET'],detail=True,url_path='run',url_name='run_case')
    # 完整的url 等于/cases/<int:case_id>/run
    def run_case(self,request,pk):  #视图函数，接收请求和接收pk
        # 获取序列化器
        case = Case.objects.get(pk=pk) #根据id获取当前的用例
        print(case)
        serialzier = self.get_serializer(instance = case)
        path = serialzier.to_json_file()

        # 执行用例，也就是利用hrun XX.json 命令行，但是有缺点，无法展示输出的结果
        # subprocess.Popen(f'hrun {path}',shell=True)

        # HR3 API的执行方法

        # 根据退出代码判断是否执行成功
        exit_code = main_run([path])
        if exit_code != 0:
            return Response(data={'error': 'failed run case', 'retcode': exit_code},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={'msg': 'run success', 'retcode': 200})


class StepViewSet(viewsets.ModelViewSet):
    '''用例步骤'''
    queryset = Step.objects.all()
    serializer_class = StepSerializer



# 文件上传
from rest_framework.parsers import FileUploadParser # 文件上传解析器
class FileUploadView(APIView):
    parser_classes = [FileUploadParser] #指定数据解析器

    def put(self,request,filename,format=None):
        # 接收文件
        file_list = request.FILES
        if not os.path.exists('upload'): # 确保project_dir/upload存在
            os.mkdir('upload')
        for k,v in file_list.items():
            with open(f'upload/{v.name}','wb') as f:
                f.write(v.read()) # 保存上传文件的内容

        # 去除http文件分隔符，前三行和最后一行
        with open(f'upload/{filename}',)as f:
            lines = f.readlines()[3:][:-1] # 过滤前三行和最后一行
        with open(f'upload/{filename}', 'w') as f:
            for line in lines:
                f.write(line)
        # 检查文件内容是否符合hr3格式
        try:
            content = loader.load_test_file(f'upload/{filename}')  # 载入文件
            valid_case = compat.ensure_testcase_v3(content) # 解析文件
        except Exception as e:
            raise serializers.ValidationError(f'错误的hr3用例格式: {repr(e)}')

        # 内容导入到数据库
        valid_case['project_id'] = 1  # 上传用例时的默认关联项目
        serializer = CaseSerializer(data=valid_case)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'retcode': 400, 'msg': 'upload failed', 'error': serializer.errors}, status=400)

        return Response({'retcode': 204, 'msg': 'uploading..'})











@swagger_auto_schema(method='GET',operation_summary='用户定制化接口摘要信息',operation_description='用户定制化接口描述信息....')
@api_view(['GET'])
# 用户定制的接口
def customer_api(request):
    return Response(data={"retcode":status.HTTP_200_OK,"msg":"testing..."})