#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 使用traceback打印异常栈 (三种方式打印结果一样-方便调试)
:Owner: jiajing_qu
:Create time: 2019/9/25 15:52
"""
import traceback
import time
import sys


def func(a,b):
    return a/b


if __name__ == '__main__':
    # traceback.print_exc()
    try:
        func(1,0)
    except:
        traceback.print_exc()
    finally:
        time.sleep(2)
        print('---------------------------')

    # print(traceback.format_exc())
    try:
        func(1,0)
    except:
        print(traceback.format_exc())
    finally:
        time.sleep(2)
        print('---------------------------')

    # traceback.print_exception(*sys.exc_info())
    try:
        func(1,0)
    except:
        traceback.print_exception(*sys.exc_info())
    finally:
        print('先finally再except')
