#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 查看hive表注释和字段注释
:Owner: jiajing_qu
:Create time: 2019/12/12 14:30
"""
from pyhive import hive
from BigData.learn_and_tests.Spark.utils.Base_Spark import Base_Spark


hive_cursor = hive.connect(host='192.168.1.101').cursor()
spark = Base_Spark()

table_list = []

for i in table_list:
    sql = "SHOW TBLPROPERTIES %s ('comment')" % i
    hive_cursor.execute(sql)
    tb_comm = hive_cursor.fetchall()[0][0]
    print(tb_comm)
    res = spark.sql('desc %s' % i)
    print(i)
    print(res.show(100,False))