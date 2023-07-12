# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/5 12:08
Author : 王新科
File : tes.py
software : PyCharm
============================
"""
# dic = {'admin_cod':''}
#
# if dic.get('admin_code')  and  dic['admin_cod'] != 'sqtp':
#     print(dic.get('admin_code'))




# name = dic.pop('name')
# print(name)


# python的反射

# class A:
#     admin_cod = 1
#     name = 2
#
# a = A()
# dic2 = {'admin_cod':'sqtp','name':'wangxinke'}
#
# for k,v in dic2.items():
#     setattr(a,k,v)
#
# print(a.admin_cod)



'''
Python编程求：一个球从100m高度自由落下，每次落地后反跳回原高度的一半，再落下，反弹，求在第十次落地时，共经过多少米，第十次反弹多高
一个球从300米的高度落下，每次会反弹距离的四分之一。当球完全静止时（距离大约等于0.00001米），球的总运行距离和弹跳次数是多少？
'''

# sn = 300
# hn = sn/4
# for n in range(2,100):
#     if hn > 0.00001:
#         sn = sn + 2 * hn  # 第n次落地时共经过的米数
#         hn = hn / 4  # 第n次反跳高度
#     elif hn <= 0.00001:
#         print(f'弹跳了{n}次数')
#         break
# print(f"总共的米数:{sn}")



# class Countball:
#     '''一个球从300米的高度落下，每次会反弹距离的四分之一。当球完全静止时（距离大约等于0.00001米），球的总运行距离和弹跳次数是多少？'''
#     n = 0
#     def __init__(self,sn,staticheight):
#         self.sn = sn
#         self.hn = self.sn / 4
#         self.staticheight = staticheight
#
#     def mainsteps(self):
#         while self.hn > self.staticheight:
#             self.sn +=  2*self.hn  # 计算n次的距离
#             self.hn = self.hn/4
#             self.n+= 1
#         print(f'目前总共弹跳的距离{self.sn} and 弹跳的次数{self.n+2}')
#         return
#
# ball = Countball(300,0.00001)
# ball.mainsteps()



import json

dicts={"name":"lucy","sex":"boy"}
json_dicts = json.dumps(dicts,indent=4)
print(json_dicts)

















