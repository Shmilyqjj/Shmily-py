#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 
:Owner: jiajing_qu
:Create time: 2019/8/23
"""
# import threading
# balance = 0
#
#
# def change_it(n):
#     global balance
#     balance = balance + n
#     balance = balance - n
#
#
# def run_thread(n):
#     for i in range(100000):
#         change_it(n)
#
#
# if __name__ == '__main__':
#     t1 = threading.Thread(target=run_thread,args=(3,))
#     t2 = threading.Thread(target=run_thread,args=(5,))
#     t1.start()
#     t2.start()
#     #  Join方法：如果一个线程在执行过程中要调用另外一个线程
#     #  并且等到其完成以后才能接着执行
#     #  那么在调用这个线程时可以使用被调用线程的join方法。
#     t1.join()
#     t2.join()
#     print(balance)





import threading
balance = 0
lock = threading.Lock()


def change_it(n):
    global balance
    balance = balance + n
    balance = balance - n


def run_thread(n):
    for i in range(100000):
        lock.acquire()  # 获取锁
        # noinspection PyBroadException
        try:
            change_it(n)
        finally: # Try -Finally确保锁一定被释放
            lock.release() # 释放锁

if __name__ == '__main__':
    t1 = threading.Thread(target=run_thread,args=(3,))
    t2 = threading.Thread(target=run_thread,args=(5,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)