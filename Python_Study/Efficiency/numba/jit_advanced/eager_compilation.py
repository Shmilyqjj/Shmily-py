#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 手动指定变量类型，加快编译速度
:Author: 佳境Shmily
:Create Time: 2020/7/24 17:08
:File: eager_compilation
:Site: shmily-qjj.top

原生Python速度慢的另一个因素是变量类型不确定，Python解释器需要进行大量的类型推断
numba同样要推断类型
如果指定已知的类型就会加快编译速度


这样不会加快执行速度，但是会加快编译速度，可以更快将函数编译到机器码上。
"""
from numba import jit, int32

# 括号内是输入，括号左侧是输出


@jit("int32(int32, int32)", nopython=True)
def f2(x, y):
    return x + y

