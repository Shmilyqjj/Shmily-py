#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: threading
:Owner: jiajing_qu
:Create time: 2019/8/23
"""


import threading,time

def loop():
    print('%s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('%s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('%s ended.' % threading.current_thread().name)


print('%s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()   #  Join方法：如果一个线程在执行过程中要调用另外一个线程，并且等到其完成以后才能接着执行，那么在调用这个线程时可以使用被调用线程的join方法。
print('%s ended.' % threading.current_thread().name)

