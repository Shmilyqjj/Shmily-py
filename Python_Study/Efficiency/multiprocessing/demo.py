#!/usr/bin/env python
# encoding: utf-8
"""
:Description: demo代码
:Author: 佳境Shmily
:Create Time: 2020/7/26 21:43
:File: demo
:Site: shmily-qjj.top
"""
import multiprocessing


def method(num):
    print(num)


if __name__ == '__main__':
    for i in range(100):
        p = multiprocessing.Process(target=method, args=(i,))
        p.start()
