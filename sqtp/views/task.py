# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/25 23:31
Author : 王新科
File : task.py
software : PyCharm
============================
"""
import uuid
import subprocess
from sqtp.models import Plan,Report
from sqtp.pagination import MyPageNumberPagination
from sqtp.serializers import PlanSerializer,ReportSerialzier,CaseSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes,action  # ，函数视图装饰器 @api_view
from httprunner.cli import main_run  # hrun命令行相关的处理
from sqtp.utils import setup_case_dir,setup_logs_dir,collect_log


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    # # 同步创建者
    # def perform_create(self, serializer):
    #     serializer.save()
    #
    # # 同步更新者
    # def perform_update(self, serializer):
    #     serializer.save()

        # 同步创建者
    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)

        # 同步更新者
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)



    # 定义运行测试计划方法,批量运行测试用例并生成测试报告
    @action(methods=['GET'], detail=True, url_path='run', url_name='run_plan')
    def run_plan(self, request, pk):
        # 获取测试计划
        plan = Plan.objects.get(pk=pk)
        # 更新计划状态--执行中
        plan.status = 1
        plan.save()
        setup_case_dir('testcase')  # 执行前清空用例目录    暂时先不清理【hrun有个小bug，无法看到清除后的文件】
        setup_logs_dir('logs') # 清空日志文件
        # 取出关联的测试用例，执行这些测试用例
        case_list = []  # 用例路径
        for case in plan.cases.all():  # 生成测试用例文件，再收集用例路径
            cs = CaseSerializer(instance=case)
            path = cs.to_json_file()
            case_list.append(path)
        # 采用uuid创建报告路径
        allure_path = f'report/{uuid.uuid4()}'
        # hr3执行用例路径列表
        # pytest入参列表规则 路径1，路径2，路径3....参数1,参数2...
        if case_list:
            exit_code = main_run([*case_list, f'--alluredir={allure_path}'])
        else:
            return Response(data={'msg': 'no cases to run', 'retcode': 304}, status=304)

        # 缓存文件转化为allure报告(index.html)
        subprocess.Popen(f'allure generate {allure_path} -o dist/{allure_path}', shell=True)

        # 更新测试计划执行状态和执行次数
        plan.status = 3
        plan.exec_counts += 1  # 执行次数+1
        plan.save()

        # 获取日志
        detail = collect_log('logs')       # logs是相当于根目录
        # 保存报告数据
        Report.objects.create(plan=plan, path=f'{allure_path}/index.html', trigger=request.user, detail=detail)

        # 根据推出代码判断是否执行成功
        if exit_code != 0:
            return Response(data={'error': 'failed run plan', 'retcode': exit_code}, status=500)
        return Response(data={'msg': 'run success', 'retcode': 200})



# class ReportViewSet(viewsets.ModelViewSet):
# ReadOnlyModelViewSet 报告只提供查询功能,说白了就是不用其他的接口，因为rest框架会自己提供其他post put delete之类的方式
class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerialzier
    pagination_class = MyPageNumberPagination # 局部分页器

    # 报告只提供查询功能
    def create(self, request, *args, **kwargs):
        return Response(data={'msg':'error','retcode':404,'error':'创建功能只针对测试计划开放'},status=404)
    # 报告更新的功能
    def update(self, request, *args, **kwargs):
        return Response(data={'msg':'error','retcode':404,'error':'更新功能只针对测试计划开放'},status=404)