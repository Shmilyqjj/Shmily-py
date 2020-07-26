#!/usr/bin/env python
# encoding: utf-8
"""
:Description: hit两种模式
:Author: 佳境Shmily
:Create Time: 2020/7/26 13:18
:File: object_onpython_mode
:Site: shmily-qjj.top

1.object模式即@jit如果遇到不支持会退化为原来的编译模式
2.nopython模式即@jit(nopython=True),加速代码，如果遇到不支持会抛异常
"""
from numba import jit


@jit
def aaa():
    pass


@jit(nopython=True)
def bbb():
    pass

