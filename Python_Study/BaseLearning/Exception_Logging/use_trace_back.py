#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 打印调用栈，追溯代码位置
:Owner: jiajing_qu
:Create time: 2020/1/8 23:15
"""
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def a():
    a =  '\n'.join(traceback.format_stack())
    print(a)
    print(type(a))

def b():
    a()
if __name__ == '__main__':
    b()