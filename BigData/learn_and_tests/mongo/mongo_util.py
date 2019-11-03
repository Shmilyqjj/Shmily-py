#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: MongoDB 工具类  未完成
:Owner: jiajing_qu
:Create time: 2019/11/1 14:04
"""
import pymongo

class mongo_util:
    """
    MongoDB 工具类
    """
    def __init__(self, host, port):
        self._client = pymongo.MongoClient(host=host, port=port)

