# -*- coding: UTF-8 -*-

# Python定时调度
# threading 模块中的 Timer 是一个非阻塞函数，比 sleep 稍好一点

from datetime import datetime
from threading import Timer


# 打印时间函数
def print_time(inc):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    t = Timer(inc, print_time, (inc,))
    t.start()


# 2s
print_time(2)
print_time(2)
