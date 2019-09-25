#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 正常的异常处理过程
:Owner: jiajing_qu
:Create time: 2019/9/25 15:51
"""
import time


def return_test(a,b):
    try:
        func(a,b)
        return 'try'
    except Exception as e:
        print(type(e))
    finally:
        return 'finally'


def func(a,b):
    print(a/b)

if __name__ == '__main__':
    try:
        func(1,0)
    except Exception as e:
        print(type(e))
        time.sleep(3)
        print(e)
    print('---------------------------')

    time.sleep(1)
    try:
        func(1,1)
    finally:
        print('exit')

    print('---------------------------')
    time.sleep(1)
    print(return_test(1, 1))

