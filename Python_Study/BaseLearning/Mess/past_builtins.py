#!/usr/bin/env python
# encoding: utf-8
"""
:Description:
:Author: 佳境Shmily
:Create Time: 2020/3/25 23:01
:File: past_builtins
:Site: shmily-qjj.top
"""


from past.builtins import *

def raw_input():
    """
    py2中
    raw_input()将所有输入作为字符串看待，并且返回字符串类型
    input()只用于数字的输入，返回所输入数字类型

    python3中，只存在input()函数，接收任意类型的输入，并且将输入默认为字符串类型处理，返回字符串类型。
    """
    from past.builtins import raw_input
    ri = raw_input()
    print("raw_input", type(ri))
    i = input()
    print("input", type(i))

def base_string():
    """
    str和basestring区别
    """
    from past.types.basestring import basestring
    print(isinstance('sss', basestring),isinstance('abc', str))
    isinstance(u'3.0', unicode)  # True
    isinstance('3.0', str)  # True
    isinstance(u'3.0', str)  # False
    isinstance(u'3.0', basestring)  # True
    isinstance('3.0', basestring)  # True

if __name__ == '__main__':
    # raw_input()
    base_string()