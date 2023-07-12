# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/25 21:40
Author : 王新科
File : demo11.py
software : PyCharm
============================
"""


from pprint import pprint # 格式化打印

# 过滤参数  接受字典的格式参数，过滤掉不变要和非空的字段
def filter_data(data):
    # 准备hr3模板比对
    template = {
        'config': {
            'name': str,
            'base_url': str,
            'variables': dict,
            'parameters': dict,
            'verify': bool,
            'export': list
        },
        'teststeps': [{
            'name': str,
            'variables': list,
            'extract': dict,
            'validate': list,
            'setup_hooks': list,
            'teardown_hooks': list,
            'request': {
                'method': str,
                'url': str,
                'params': list,
                'headers': dict,
                'cookies': dict,
                'data': dict,
                'json': dict
            },
        }]
    }

    return merge_dict(template,data)

def merge_dict(left,right):
    '''合并字典同类项目,删除空格的数据'''
    # 覆盖左侧模板的同类项目

    for k in right:
        if k in left:
            if isinstance(left[k],dict) and isinstance(right[k],dict):
                merge_dict(left[k],right[k])
            elif isinstance(left[k], list) and isinstance(right[k], list):
                for one in right[k]:
                    merge_dict(left[k][0], one)

            elif right[k]:  # 不为空(也包含空字符串，空列表，空字典)
                left[k] = right[k]
            elif not right[k]: # if为空
                left.pop(k) #删除左侧对应又饿为空的数据

    # 删除左侧多余项目  字典不支持一边遍历，一边删除。我给他个list临时对象，就可以删除了
    for k in list(left.keys()):
        if k not in right:
            left.pop(k)

    return left # left是最好处理好的数据


if __name__ == '__main__':
    template = {
        'config': {
            'name': str,
            'baseurl': str,
            'variables': dict,
            'parameters': dict,
            'verify': bool,
            'export': list
        },
        'teststeps': [{
            'name': str,
            'variables': list,
            'extract': dict,
            'validate': list,
            'setup_hooks': list,
            'teardown_hooks': list,
            'request': {
                'method': str,
                'url': str,
                'params': list,
                'headers': dict,
                'cookies': dict,
                'data': dict,
                'json': dict
            },
        }]
    }
    data = {
    "config": {
        "project": {
            "id": 1,
            "admin": None,
            "name": "测开",
            "status": 0,
            "version": "v1",
            "desc": "测开3期",
            "create_time": "2022-09-12 14:45:08",
            "update_time": "2022-09-12 14:45:08"
        },
        "name": "小米手机发布会",
        "baseurl": 'loclhost',
        "variables": {},
        "parameters": {},
        "verify": False,
        "export": []
    },
    "teststeps": [
        {
            "name": "step_name",
            "variables": {},
            "request": {
                "method": "GET",
                "url": "/demo/path",
                "params": {},
                "headers": {},
                "json": {},
                "data": {}
            },
            "extract": {},
            "validate": [],
            "setup_hooks": [],
            "teardown_hooks": [],
            "belong_case_id": 13,
            "sorted_no": 1
        }
    ],
    "desc": "gest01",
    "id": 13,
    "file_path": "测开_小米手机发布会.json",
    "create_time": "2022-09-19T17:21:42.328050Z",
    "update_time": "2022-09-25T14:05:39.932171Z"
}
    res = merge_dict(template,data)
    pprint(res)



