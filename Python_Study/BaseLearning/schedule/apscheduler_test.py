# -*- coding: UTF-8 -*-

"""
:Description: APScheduler 四个组件分别为：触发器(trigger)，作业存储(job store)，执行器(executor)，调度器(scheduler)。
:Owner: shmily
:Create time: 2022/9/5 14:09

触发器(trigger)
包含调度逻辑，每一个作业有它自己的触发器，用于决定接下来哪一个作业会运行。除了他们自己初始配置意外，触发器完全是无状态的
APScheduler 有三种内建的 trigger:
  date: 特定的时间点触发
  interval: 固定时间间隔触发
  cron: 在特定时间周期性地触发

作业存储(job store)
存储被调度的作业，默认的作业存储是简单地把作业保存在内存中，其他的作业存储是将作业保存在数据库中。一个作业的数据讲在保存在持久化作业存储时被序列化，并在加载时被反序列化。调度器不能分享同一个作业存储。
APScheduler 默认使用 MemoryJobStore，可以修改使用 DB 存储方案

执行器(executor)
处理作业的运行，他们通常通过在作业中提交制定的可调用对象到一个线程或者进城池来进行。当作业完成时，执行器将会通知调度器。
最常用的 executor 有两种：
  ProcessPoolExecutor
  ThreadPoolExecutor

调度器(scheduler)
通常在应用中只有一个调度器，应用的开发者通常不会直接处理作业存储、调度器和触发器，相反，调度器提供了处理这些的合适的接口。配置作业存储和执行器可以在调度器中完成，例如添加、修改和移除作业。

pip3 install apscheduler
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == '__main__':
    # 定义BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(job, 'interval', seconds=2)
    sched.add_job(job, 'interval', seconds=3)
    sched.start()
    # 上述代码创建了一个 BlockingScheduler，并使用默认内存存储和默认执行器。
    # (默认选项分别是 MemoryJobStore 和 ThreadPoolExecutor，其中线程池的最大线程数为10)。
    # 配置完成后使用 start() 方法来启动。
