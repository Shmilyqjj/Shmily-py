# encoding=utf-8

import threading
import time



class myThread(threading.Thread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadId = threadID
        self.name = name
        self.counter = counter
    def run(self):    #线程创建执行run函数
        while self.counter < 8:
            time.sleep(2)
            self.counter += 1
            print self.threadId,self.name,self.counter,time.ctime(time.time())
            print
        print("Thread Stop")


thread1 = myThread(1,"Thread-1",1)
thread2 = myThread(2,"Thread-2",2)

thread1.start()
thread2.start()

