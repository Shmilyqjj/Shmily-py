# -*- coding: UTF-8 -*-

"""
:Description: sched模块是 Python 内置的模块，它是一个调度（延时处理机制），每次想要定时执行某任务都必须写入一个调度。
:Owner: shmily
:Create time: 2022/9/5 14:09
"""

import sched
import time
from datetime import datetime
# 初始化sched模块的 scheduler 类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)


# 被周期性调度触发的函数
def printTime(inc):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    schedule.enter(inc, 0, printTime, (inc,))


def printTime1(inc):
    print(datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
    schedule.enter(inc, 0, printTime1, (inc,))


if __name__ == '__main__':
    # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    # 给该触发函数的参数（tuple形式）
    schedule.enter(0, 0, printTime, (2,))
    schedule.enter(0, 0, printTime1, (3,))
    schedule.run()

