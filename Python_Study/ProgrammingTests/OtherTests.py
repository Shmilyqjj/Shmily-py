#!/usr/bin/python3
# -*- coding:utf-8 -*-
#全局变量 函数内改变函数外变量的方法
import re
import os
#
# count = 0
# def xyz():
#     global count
#     while (count < 10):
#         count = count + 1
#     print(count)
#
# xyz()
# print(count)
#
# res = 'https://www.%s.com/%s/%s/%d' % ('baidu','abc','def',8)
# print(res)
#
#
# s = 'e7\\xad\\x89\\xe6\\x93\\x8d\\xe4\\xbd\\x9c\\r\\n\\r\\n\\r\\nimport os\\r\\nimport re\\r\\n\\r\\n\\r\\n\\r\\nPROJECT_PATH = \'C:\\\\\\\\Users\''
# re.match(r'.*import.*', s)
#
# list0 = [1,5,7,6,8,4,2,3]
# print(sorted(list0))
# print(sorted(list0,reverse=True))

##############################################################################

# p = [1,2,4,5,6,7]
# def abc(paras):
#     def cde(paras):
#         print(paras[0])
#     return cde(paras)

# 查目录下四字节的文件
# def find_files():
#     file_list = []
#     path = 'D:\\'
#     for root, dirs, f in os.walk(path):
#         paths = [os.path.join(root, name) for name in f]
#         if len(paths) != 0:  # 文件数不为0
#             for name in paths:
#                 if os.path.getsize(name) == 4:
#                     file_list.append(name)
#     return file_list

##############################################################################


# class A(object):
#     """
#     Class A.
#     """
#
#     a = 0
#     b = 1
#
#     def __init__(self):
#         self.a = 2
#         self.b = 3
#
#     def test(self):
#         print 'a normal func.'
#
#     @staticmethod
#     def static_test(self):
#         print 'a static func.'
#
#     @classmethod
#     def class_test(self):
#         print 'a calss func.'
#
# if __name__ == '__main__':
#     # abc(p)
#     pass
#     a = A()
#     print A.__dict__
#     # print a.__dict__
#     print(hasattr(a, '__doc__'))
#     print(a.__dict__)
#     m = getattr(a, 'test')
#     m()

##############################################################################
# import json
# fo = open(r'C:\Users\Home-PC\PycharmProjects\Shmily-py\Python_Study\ProgrammingTests\out.log', 'a+')
# info = fo.read()
# # print(info)
# print(json.loads(info))
# d = {"1":"2","2": "2"}
# fo.write(str(d))
##############################################################################


















################################
