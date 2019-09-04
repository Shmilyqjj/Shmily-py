#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description:  死循环
:Owner: jiajing_qu
:Create time: 2019/8/23
"""
import multiprocessing
import threading


def loop():
    x = 0
    while True:
        x = x ^ 1
        print(x)


for i in range(multiprocessing.cpu_count()):
    # 一个死循环 会占满一个CPU核心 100%
    t1 = threading.Thread(target=loop)
    t1.start()
