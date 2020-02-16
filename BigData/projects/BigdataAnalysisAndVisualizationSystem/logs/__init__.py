#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
Description:日志统一输出路径
Author:曲佳境
Date: 2019/12/14 1:11
"""

"""
标准控制台日志输出格式
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

筛选日志写入log文件 输出格式
def logging_print():
    logging.basicConfig(filename="test.log", filemode="a", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)    # 会将DEBUG级别及以上的日志记录写入文件
    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')

后面编写logging通用模块
"""
