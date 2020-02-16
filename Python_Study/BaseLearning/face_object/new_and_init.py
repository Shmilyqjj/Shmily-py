#!/usr/bin/env python
# encoding: utf-8
"""
:Description:
:Author: jiajing_qu
:Create Time: 2020/2/16 19:57
:File: new_and_init.py
:Site: shmily-qjj.top
"""

import time

class A(object):

    def __init__(self, c, day):
        self.day = day
        self.c = c
        print("正在初始化和完善对象")
        time.sleep(2)
        print(self.day)

    def __new__(cls, *args):
        print(args)
        if args[len(args)-1] == -1:
            print -1
            return
        else:
            # 直接返回父类的new方法 对象生成是在 new 里面 的return （返回一个对象）
            return super(A, cls).__new__(cls)

    def __del__(self):
        print("正在删除对象")
        time.sleep(2)

if __name__ == '__main__':
    a = A(2, -1)
    print("*****************************")
    a = A(2, 1)