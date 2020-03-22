#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 得到数据库中某几个库或者全部库的所有表,以及表信息
:Owner: jiajing_qu
:Create time: 2019/11/4 15:26
"""
try:
    import MySQLdb
    import MySQLdb.cursors
except ImportError:
    import pymysql as MySQLdb

from pyhive import hive

def get_mysql_connect(ip, user, password, port, database, charset='utf8', connect_timeout=8):
    return MySQLdb.connect(host=ip,
                               user=user,
                               passwd=password,
                               port=int(port),
                               charset=charset,
                               connect_timeout=connect_timeout,
                               db=database,
                               cursorclass=MySQLdb.cursors.DictCursor)


def get_hive_connect(host='192.168.1.101'):
    conn = hive.connect(host)
    return conn


def get_all_tables(cur):
    cur.execute("show tables")
    return cur.fetchall()


if __name__ == '__main__':
    connection = get_mysql_connect("localhost", "root", "123456", 3306, "sql_test")
    cur = connection.cursor()
    print(get_all_tables(cur))
    get_hive_connect()

