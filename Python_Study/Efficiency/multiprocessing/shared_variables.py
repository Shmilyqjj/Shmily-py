#!/usr/bin/env python
# encoding: utf-8
"""
:Description:multiprocessing 共享变量 多进程共享内存
:Author: 佳境Shmily
:Create Time: 2020/7/26 22:00
:File: shared_variables
:Site: shmily-qjj.top

multiprocessing.Value(typecode_or_type, *args[, lock])
multiprocessing.Array(typecode_or_type, size_or_initializer, *, lock=True)
"""
import multiprocessing
from ctypes import c_char_p
import time
int_val = multiprocessing.Value('i', 0)   # int类型共享变量
s = (c_char_p, 'str')  # str类型共享变量


def method(num):
    for i in range(10):
        time.sleep(0.1)
        with int_val.get_lock():  # 仍然需要使用 get_lock 方法来获取锁对象
            int_val.value += num
        print(int_val.value)


if __name__ == '__main__':
    for i in range(100):
        p = multiprocessing.Process(target=method, args=(i,))
        p.start()



