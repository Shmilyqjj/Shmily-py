#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 得到数据库中某几个库或者全部库的所有表,以及表信息
:Owner: jiajing_qu
:Create time: 2019/11/4 15:26
"""
import pymysql
from pyhive import hive

def get_mysql_connect():
    pymysql.connect()


def get_hive_connect():
    hive.connect()


def get_all_tables():
    pass

