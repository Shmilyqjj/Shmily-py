#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 
:Owner: jiajing_qu
:Create time: 2019/9/6 10:29
"""

import os
import datetime
import time
import shutil
LOG_FILE_PATH = '/data/logs/streaming_monitor/monitor.log'
HISTORY_LOG_PATH = '/data/logs/streaming_monitor/history'
LOG_DIR_PATH = '/data/logs/streaming_monitor'
MAX_LOG_SIZE = 10485760   # 10M


def logs_manager():
    """
    管理日志文件（自动清理）
    日志文件位置LOG_FILE_PATH = '/data/logs/streaming_monitor/monitor.log'
    达到10M时移入HISTORY_LOG_PATH = '/data/logs/streaming_monitor/history'
    七天后删除HISTORY_LOG
    """
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    mkdir(LOG_DIR_PATH)
    if os.path.exists(LOG_FILE_PATH):
        file_size = os.path.getsize(LOG_FILE_PATH)
        if file_size >= MAX_LOG_SIZE:
            shutil.move(LOG_FILE_PATH, '%s/%s_monitor.log' % (HISTORY_LOG_PATH, now_time))
            print('日志达到%d字节，移入%s' % (MAX_LOG_SIZE, HISTORY_LOG_PATH))
    if len(os.listdir(HISTORY_LOG_PATH)) != 0:  # 文件数不为0
        for name in os.listdir(HISTORY_LOG_PATH):
            now_timestamp = time.time()
            alter_timestamp = os.path.getmtime('%s/%s' % (HISTORY_LOG_PATH, name))
            if now_timestamp - alter_timestamp >= 604800:
                os.remove('%s/%s' % (HISTORY_LOG_PATH, name))
                print('历史日志文件过期,删除%s文件' % name)
