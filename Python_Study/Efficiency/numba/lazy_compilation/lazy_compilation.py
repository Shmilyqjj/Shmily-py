#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 懒编译测试  可得编译时间
:Author: 佳境Shmily
:Create Time: 2020/7/24 16:56
:File: lazy_compilation
:Site: shmily-qjj.top

在运行过程中第一次发现源代码中有@jit，才将该代码块编译；
同一个Numba函数多次调用，只需要编译一次；
"""

from numba import jit
import numpy as np
import time

SIZE = 10000
x = np.random.random((SIZE, SIZE))


"""
给定n*n矩阵，对矩阵每个元素计算tanh值，然后求和。
因为要循环矩阵中的每个元素，计算复杂度为 n*n。
"""


@jit
def jit_tan_sum(a):   # 函数在被调用时编译成机器语言
    tan_sum = 0
    for i in range(SIZE):   # Numba 支持循环
        for j in range(SIZE):
            tan_sum += np.tanh(a[i, j])   # Numba 支持绝大多数NumPy函数
    return tan_sum

# 总时间 = 编译时间 + 运行时间
start = time.time()
jit_tan_sum(x)
end = time.time()
print("Elapsed (with compilation) = %s" % (end - start))


# Numba将加速的代码缓存下来，无需再次编译
# 总时间 = 运行时间
start = time.time()
jit_tan_sum(x)
end = time.time()
print("Elapsed (after compilation) = %s" % (end - start))