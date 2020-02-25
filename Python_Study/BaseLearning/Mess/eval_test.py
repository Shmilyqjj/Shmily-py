#!/usr/bin/env python
# encoding: utf-8
"""
:Description:  eval方法测试
:Author: jiajing_qu
:Create Time: 2020/2/25 12:01
:File: eval_test
:Site: shmily-qjj.top
"""

dic_str = '{"field_name":"","primary_key":"","extract_type":"odps_full"}'
dic = eval(dic_str)
print(dic,type(dic))

x = 7
print(eval( '3 * x' ))

print(eval('pow(2,2)'))

print(eval('2 + 2'))

n=81
print(eval("n + 4"))
