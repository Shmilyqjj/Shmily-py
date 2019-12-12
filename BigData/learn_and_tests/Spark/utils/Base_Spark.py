#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 提供spark session或者sqlContext
:Owner: jiajing_qu
:Create time: 2019/12/12 14:35
"""
from pyspark.sql import HiveContext
from pyspark import SparkContext, SparkConf
def Base_Spark(name=None, config=None, context=False):
    """
    Get spark object.
    :param name: string. The name of the spark task.
    :param config: dict. The config of the spark task.
    :param context: boole. 如果想拿到sqlContext就给True.
    :return: spark object.
    """
    conf = SparkConf()

    if config:
        for k,v in config.items():
            conf.set(k,v)
    else:
        config = {}

    sc = SparkContext(conf=conf,appName= name if name else None)
    sc.setLogLevel("WARN")
    sqlContext = HiveContext(sc)

    if config:
        for k,v in config.items() :
            if 'hive.' in k:
                sqlContext.setConf(k,v)
    if context:
        return sqlContext
    else:
        spark = sqlContext.sparkSession
        return spark