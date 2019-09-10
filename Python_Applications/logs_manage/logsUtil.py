#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 日志文件管理
:Owner: jiajing_qu
:Create time: 2019/9/6 10:29
"""
import os
import datetime
import time
import shutil

"""
输入格式：
log_path = '/data/airflow/logs'  日志路径
log_files = ['webserver.log','scheduler.log']   日志文件名
max_size = 512   # 512MB  阈值
days = 0.1  清空历史日志的天数
"""


def logs_manager(log_path, log_files, max_size, days):
    """
    日志文件管理
    :param log_path: 日志所在路径
    :param log_files:日志文件名 list
    :param max_size: max日志大小
    :param days:     历史日志过期时间
    :return:
    """

    if os.path.exists(log_path):
        global history_log_dir
        history_log_dir = log_path + '/log_history/'
        if not os.path.exists(history_log_dir):
            os.mkdir(history_log_dir)
            print("创建日志文件夹 %s" % history_log_dir)
        for file_name in log_files:
            source = log_path + '/' + file_name
            if os.path.exists(source):
                file_size = os.path.getsize(source) / 1024 / 1024  # b转mb
                if file_size >= max_size:
                    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    target = history_log_dir + file_name + '_' + now_time
                    try:
                        shutil.move(source, target)
                        print('日志达到%d MB,存为%s文件' % (max_size, target))
                    except Exception as e:
                        print('移动日志文件失败', e)
            else:
                print('%s文件不存在' % file_name)
            # 定期删除
            for root, dirs, f in os.walk(history_log_dir):
                paths = [os.path.join(root, name) for name in f]
                if len(paths) != 0:  # 文件数不为0
                    for name in paths:
                        now_timestamp = time.time()
                        alter_timestamp = os.path.getmtime(name)
                        if now_timestamp - alter_timestamp >= 86400 * days:
                            os.remove(name)
                            print('历史日志文件过期,删除%s文件' % name)
    else:
        os.mkdir(log_path)



# @auto_batch2
def main(para=None):
    log_path = para.get('log_path')
    log_files = para.get('log_files')
    max_size = para.get('max_size')
    days = para.get('days')
    logs_manager(log_path, log_files, max_size, days)


if __name__ == '__main__':
    main()
