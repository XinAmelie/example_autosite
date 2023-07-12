# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/4 12:28
Author : 王新科
File : exception.py
software : PyCharm
============================
"""
################################################异常处理器#############################################
# 处理异常的返回

# exception_handler获取标准的错误响应
from rest_framework.views import exception_handler,Response
from rest_framework import exceptions

def my_exception_handler(exc,context):  # exceptions.APIException api层面的异常
    '''
    获取标准的错误响应
    exc:异常信息
    context 上下文
    '''
    error_response = exception_handler(exc,context)
    print('走这不了吗？？')
    print(error_response)
    if error_response:
        if isinstance(exc,exceptions.APIException):
            error_msg = exc.detail
        else:
            error_msg = exc  # 404 permission_denied

        error_response.data = {
            'msg':'error',
            'retcode': error_response.status_code,
            'error': str(error_msg)
        }

    return error_response

