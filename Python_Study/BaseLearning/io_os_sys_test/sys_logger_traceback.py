#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
Description: sys+logger来提供报错信息，方便查错
Author:曲佳境
Date: 2020/1/14 21:51
"""
import sys
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("这步报错了，下面打印报错的文件和行号")
print(sys._getframe().f_lineno - 1)
print(sys._getframe().f_code.co_filename)

logger.error("Error In File: %s Line: %s" % (sys._getframe().f_code.co_filename, sys._getframe().f_lineno - 1))
