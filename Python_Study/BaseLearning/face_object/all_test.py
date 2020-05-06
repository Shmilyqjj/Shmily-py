#!/usr/bin/env python
# encoding: utf-8
"""
:Description: all and  __all__
:Author: 佳境Shmily
:Create Time: 2020/5/6 8:49
:File: all_test
:Site: shmily-qjj.top
"""


# 未定义__all__属性时 from xx import *可以导入所有公共属性 方法 和类
# 定义__all__属性时 from xx import * 只能导入all内指定的属性，方法和类（all内可指定私有变量，方法，属性）

"""
注意： from xx import * 只能导入公有属性，方法或类 不能导入带_和__的protect和private类型
注意：__all__只能影响到from xx import *不能影响到 from xx import xxx
"""
__all__ = ('A', 'func')  # 外部只能导入A类和func方法
class A(object):
    def __init__(self):
        pass

class B(object):
    pass

def func():
    print(1)


if __name__ == '__main__':
    # all 方法用于判断给定的iterable集合（list or tuple）中的所有元素是否都为True，是则返回True 不是则false (0,"",None,False都算False)
    print(all([1, 2, 3, 4, 5]))
    print(all([1, 2, 0, 4, 5]))
    print(all(["", 2, 0, 4, 5]))
    print(all(["3", "2", 1, 4, 5]))
    print(all(("3", "2", None, 4, 5)))