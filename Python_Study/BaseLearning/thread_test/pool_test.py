#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: thread pool加速for循环中的操作
:Owner: jiajing_qu
:Create time: 2019/12/31 10:53

multiprocessing包是Python中的多进程管理包。它与 threading.Thread类似，可以利用multiprocessing.Process对象来创建一个进程。该进程可以允许放在Python程序内部编写的函数中。该Process对象与Thread对象的用法相同，拥有is_alive()、join([timeout])、run()、start()、terminate()等方法。
这个模块表示像线程一样管理进程，这个是multiprocessing的核心，它与threading很相似，对多核CPU的利用率会比threading好的多。
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
