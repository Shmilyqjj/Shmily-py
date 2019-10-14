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
import logging
import traceback


"""
输入格式：
log_path = '/data/airflow/logs'  日志路径
log_files = ['webserver.log','scheduler.log']   日志文件名 (可选)
max_size = 512   # 512MB  阈值  (可选)
days = 0.1  清空历史日志的天数
"""


def rm_empty_dirs(dir_path):
    """
    递归删除路径下所有空文件夹
    :param dir_path: 文件夹路径
    :return:
    """
    for root, dirs, f in os.walk(dir_path):
        dir_paths_list = [os.path.join(root, d) for d in dirs]
        if len(dir_paths_list) != 0:
            for dir_path in dir_paths_list:
                if len(os.listdir(dir_path)) == 0:
                    os.rmdir(dir_path)
                    logging.info('删除了空文件夹 %s' % dir_path)
                else:
                    rm_empty_dirs(dir_path)


def logs_manager(log_path, days, max_size=0, log_files=None):
    """
    日志文件管理
    :param log_path: 日志所在路径
    :param log_files:日志文件名 list(默认空则遍历所有文件)
    :param max_size: max日志大小(默认为0表示过期直接删除)
    :param days:     历史日志过期时间
    :return:
    """
    global history_log_dir
    sec = 86400 * days  # 秒
    history_log_dir = log_path + '/log_history/'
    if os.path.exists(log_path):
        if max_size != 0:  # 如果指定了日志大小,创建历史日志文件夹
            if not os.path.exists(history_log_dir):
                os.mkdir(history_log_dir)
                logging.info("创建日志文件夹 %s" % history_log_dir)

        if log_files:  # 如果指定了具体文件 则不遍历全部文件
            for file_name in log_files:
                source = log_path + '/' + file_name  # 指定的日志文件的全路径
                if os.path.exists(source):
                    if max_size != 0:  # 如果指定了日志最大大小,则判断文件大小并决定是否移动到历史日志文件夹
                        file_size = os.path.getsize(source) / 1024 / 1024  # b转mb
                        if file_size >= max_size:
                            now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                            target = history_log_dir + file_name + '_' + now_time
                            try:
                                shutil.move(source, target)
                                logging.info('日志达到%d MB,存为%s文件' % (max_size, target))
                            except:
                                logging.error(traceback.format_exc())
                    else:  # 如果未指定日志大小 则直接删除过期日志
                        now = time.time()
                        alter_timestamp = os.path.getmtime(source)
                        if now - alter_timestamp >= sec:
                            try:
                                os.remove(source)
                                logging.info('历史日志文件过期,删除%s文件' % source)
                            except:
                                logging.error(traceback.format_exc())
                else:
                    logging.info('未找到指定的日志文件 %s' % source)

        if not log_files:  # 如果未指定具体日志文件则遍历路径下全部文件,并删除过期日志
            now = time.time()
            for root, dirs, f in os.walk(log_path):
                file_paths_list = [os.path.join(root, name) for name in f]
                if len(file_paths_list) != 0:
                    for file_path in file_paths_list:
                        if now - os.path.getmtime(file_path) >= sec:
                            try:
                                os.remove(file_path)
                                logging.info('历史日志文件过期,删除%s文件' % file_path)
                            except:
                                logging.error(traceback.format_exc())

            rm_empty_dirs(log_path)  # 递归删除空文件夹

        if os.path.exists(history_log_dir):  # 定期删除历史文件夹中的日志
            for root, dirs, f in os.walk(history_log_dir):
                paths = [os.path.join(root, name) for name in f]
                if len(paths) != 0:  # 文件数不为0
                    for name in paths:
                        now = time.time()
                        alter_timestamp = os.path.getmtime(name)
                        if now - alter_timestamp >= sec:
                            try:
                                os.remove(name)
                                logging.info('历史日志文件过期,删除%s文件' % name)
                            except:
                                logging.error(traceback.format_exc())
    else:
        print('%s日志路径不存在' % log_path)





# @auto_batch2
def main(para=None):
    """
    入口是函数
    :param para:
    """
    log_path = para.get('log_path')
    log_files = para.get('log_files')
    max_size = para.get('max_size')
    days = para.get('days')
    logs_manager(log_path, log_files, max_size, days)


if __name__ == '__main__':
    main()
