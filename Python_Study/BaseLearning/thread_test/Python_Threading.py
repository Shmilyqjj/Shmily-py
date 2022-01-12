#!/usr/bin/env python
# encoding: utf-8
"""
:Description:Threading运行三个不同线程
:Author: 佳境Shmily
:Create Time: 2022/1/10 14:31
:File: ThreadingTest
:Site: shmily-qjj.top
"""

import threading
import time

s = set()  # 全局变量


def a():
    for i in range(1, 5):
        if i not in s:  # 输出过的数字就不打印了
            s.add(i)  # 向集合里添加元素，不会影响数据的准确性
            print(i)
            time.sleep(30)


def b():
    for i in range(6, 10):
        if i not in s:  # 输出过的数字就不打印了
            s.add(i)  # 向集合里添加元素，不会影响数据的准确性
            print(i)
            time.sleep(20)


def c():
    for i in range(11, 15):
        if i not in s:  # 输出过的数字就不打印了
            s.add(i)  # 向集合里添加元素，不会影响数据的准确性
            print(i)
            time.sleep(1)


if __name__ == '__main__':
    threads = []
    th1 = threading.Thread(target=a, args=())
    th2 = threading.Thread(target=b, args=())
    th3 = threading.Thread(target=c, args=())
    th1.start()
    th2.start()
    th3.start()
    threads.append(th1)
    threads.append(th2)
    threads.append(th3)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("All Done")