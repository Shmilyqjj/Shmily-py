# -*- coding: UTF-8 -*-

#Python中使用线程有两种方式：函数或者用类来包装线程对象。
import thread

import time
import datetime

def print_time(threadName,delay):
    count = 0
    while count <= 5:
        time.sleep(2)
        now_time = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
        print(now_time)
        count += 1

#thread.start_new_thread ( function, args[, kwargs] ) 创建线程
try:
    thread.start_new_thread(print_time,("Thread-1",2,))
    thread.start_new_thread(print_time,("Thread-2",2,))
    thread.start_new_thread(print_time,("Thread-3",4,))
except:
    print("unable to start thread")
while 1:
    pass













