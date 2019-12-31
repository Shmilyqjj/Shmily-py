#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: thread pool加速for循环中的操作
:Owner: jiajing_qu
:Create time: 2019/12/31 10:53
"""

from multiprocessing.pool import ThreadPool


def my_print(item):
    print(item[0]+item[1])


pool_size = 10
items = [1,2,3,4,5,6,7,8,9,0,12,14,15,16,16,17,18]
items = [(1,2),(2,3),(3,4),(4,5)]

pool = ThreadPool(pool_size)  # 创建一个线程池
pool.map(my_print, items)  # 往线程池中填线程
pool.close()  # 关闭线程池，不再接受线程
pool.join()  # 等待线程池中线程全部执行完
