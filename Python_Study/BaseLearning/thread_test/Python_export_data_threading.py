#!/usr/bin/env python
# encoding: utf-8
"""
:Description:假设导表分三步 第一步建临时表 第二部下载数据 第三步拷贝数据  正常情况下三步是串行执行，现在需要多线程运行，达到最大效率，即保持三步顺序的前提下三步操作互不影响，同时进行
:Author: 佳境Shmily
:Create Time: 2022/1/10 14:31
:File: Python_export_data_threading.py
:Site: shmily-qjj.top
"""

import threading
import time

# 全局变量
full_tasks = ['task1', 'task2', 'task3', 'task4', 'task5']
all_tasks = full_tasks.copy()
tmp_table_done_queue = []
get_data_done_queue = []
all_done_list = []


def create_tmp_table():
    while 1:
        if len(all_tasks) != 0:
            task_name = all_tasks.pop(0)
            print(f"开始create_tmp_table:{task_name}")
            time.sleep(20)  # 创建临时表耗时20s
            tmp_table_done_queue.append(task_name)  # 加入已完成临时表创建的队列
            print(f"完成create_tmp_table:{task_name}")
        else:
            print(f"===========所有create_tmp_table任务完成===========")
            return


def get_data():
    while True:
        if len(tmp_table_done_queue) != 0:
            task_name = tmp_table_done_queue.pop(0)
            print(f"开始get_data:{task_name}")
            time.sleep(10)  # 下载数据耗时10s
            get_data_done_queue.append(task_name)
            print(f"完成get_data:{task_name}")
        elif len(full_tasks) != len(all_done_list):
            print(f"all_tasks:{len(all_tasks)} tmp_table:{len(tmp_table_done_queue)} get_data:{len(get_data_done_queue)} all_done:{len(all_done_list)} 等待get_data")
            time.sleep(5)
        else:
            return


def load_data():
    while 1:
        if len(get_data_done_queue) != 0:
            task_name = get_data_done_queue.pop(0)
            print(f"开始load_data:{task_name}")
            time.sleep(15)  # 加载数据耗时15s
            all_done_list.append(task_name)
            print(f"完成load_data:{task_name}")
        elif len(full_tasks) != len(all_done_list):
            print(f"all_tasks:{len(all_tasks)} tmp_table:{len(tmp_table_done_queue)} get_data:{len(get_data_done_queue)} all_done:{len(all_done_list)} 等待load_data")
            time.sleep(5)
        else:
            return


if __name__ == '__main__':
    threads = []
    th1 = threading.Thread(target=create_tmp_table, args=())
    th2 = threading.Thread(target=get_data, args=())
    th3 = threading.Thread(target=load_data, args=())
    th1.start()
    th2.start()
    th3.start()
    threads.append(th1)
    threads.append(th2)
    threads.append(th3)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print(all_tasks)
    print(tmp_table_done_queue)
    print(get_data_done_queue)
    print(all_done_list)
    print("All Done")