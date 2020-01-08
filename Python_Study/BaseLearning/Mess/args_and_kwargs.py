#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: *args 和 **kwargs
:Owner: jiajing_qu
:Create time: 2020/1/8 23:05
"""

def func_args(*args):
    # *args代表tuple
    print(args)
    print(type(args))

def func_kwargs(**kwargs):
    # **kwargs代表dict
    print(kwargs)
    print(type(kwargs))

if __name__ == '__main__':
    func_args(1,2,3,4,5,6)
    func_kwargs(q=1, p=2, j=3)