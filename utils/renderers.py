# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/4 0:36
Author : 王新科
File : renderers.py
software : PyCharm
============================
"""
from rest_framework.renderers import JSONRenderer

# 自定义渲染器
class MyRenderer(JSONRenderer):
    '''
    重构render方法
    '''
    # data序列化对象的数据   renderer_context渲染的回参数   accepted_media_type接收到的数据类型
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # return super().render(data, accepted_media_type, renderer_context)
        status_code = renderer_context['response'].status_code
        # 正常返回 status_code 以2开头
        if str(status_code).startswith('2'):
            # 处理自定义分页内容
            res = {'msg': 'success', 'retcode': status_code}  # 返回模板
            if not isinstance(data, list):
                if 'retlist' not in data:
                    res.update({'retlist': [data]})  # 单个数据的情况
                else:
                    res.update(data)  # 多个数据情况
            else:
                res.update({'retlist': data})
            return super().render(res,accepted_media_type,renderer_context)
        else: # 异常情况
            # 调用父类，把res这个值重写传给data
            return super().render(data,accepted_media_type,renderer_context)
