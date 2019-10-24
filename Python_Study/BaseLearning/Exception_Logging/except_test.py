#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 正常的异常处理过程
:Owner: jiajing_qu
:Create time: 2019/9/25 15:51
"""
import time

def raise_exception():
    """
    自定义抛出异常
    :return:
    """
    if 1>0:
        print("1>0")
        raise Exception("1>0正确的")

def return_test(a,b):
    """
    测试finally的return  与java原理相同,先finally的return 再 try的return
    :param a:
    :param b:
    :return:
    """
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

    print('---------------------------')
    time.sleep(2)
    raise_exception()

