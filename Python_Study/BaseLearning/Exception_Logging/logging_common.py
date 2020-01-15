#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
Description: logging模块快捷用法
Author:曲佳境
Date: 2020/1/14 22:08
"""
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


logger.info("info")
logger.warn("warn")
logger.error("error")