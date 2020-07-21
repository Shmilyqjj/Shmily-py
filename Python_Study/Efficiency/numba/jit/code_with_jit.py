#!/usr/bin/env python
# encoding: utf-8
"""
:Description:一段代码 使用numba的jit即时编译器
:Author: 佳境Shmily
:Create Time: 2020/7/21 19:35
:File: code_with_jit
:Site: shmily-qjj.top
"""
import time
from numba import jit


@jit
def time_com(i):
    cum = 0
    for test in range(i):
        for ind in range(i):
            cum += (test * ind) % 3


if __name__ == '__main__':
    t1 = time.time()
    for i in range(1000):
        time_com(i)
    t2 = time.time()
    print("run time:%f s" % (t2 - t1))

# run time:0.750926 s
