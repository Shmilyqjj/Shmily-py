#!/usr/bin/env python
# encoding: utf-8
"""
:Desc: 计算Linux并发执行cmd时，平均耗时
:Author: shmily
:Create Time: 2023/8/21 下午12:16
:@File: exec_cmd_concurrently_avg_time.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""
import subprocess
import time
import threading
from functools import reduce

costs = []


def exec_cmd_time(cmd, cmd_id=0):
    st = time.time()
    ret = subprocess.Popen(cmd, shell=True)
    ret.wait()
    if ret.returncode != 0 :
        raise Exception(f"cmd exec error. errMsg: ${ret.stderr}")
    time_cost = time.time() - st
    costs.append(time_cost)
    print(f"cmd{cmd_id}_cost: {time_cost}s")


if __name__ == '__main__':
    concurrency = 3
    cmd = "sleep 3"
    # cmd = "presto -f=/mnt/nas/qjj/TPC-H/dbgen/sqls/1.sql"
    threads = []
    for i in range(concurrency):
        thread = threading.Thread(target=exec_cmd_time, args=(cmd, i))
        threads.append(thread)
    for t in threads:
        t.start()
    for t in threads:
        t.join()  # 主线程等待子线程结束

    print(f"Finished. Avg cost time: {reduce(lambda x, y: x+y, costs) / len(costs)}")
