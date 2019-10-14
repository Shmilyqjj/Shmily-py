#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: Spark SQL UDF
:Owner: jiajing_qu
:Create time: 2019/10/11 19:17
"""
from pyspark import SparkContext, SparkConf, HiveContext
from pyspark.sql.types import *

def get_spark_session():
    conf = SparkConf()
    sc = SparkContext(conf=conf,appName='UDF_TEST')
    sc.setLogLevel("WARN")
    sqlContext = HiveContext(sc)
    spark = sqlContext.sparkSession
    return spark

def length(ip):
    if ip:
        return len(ip)
    else:
        return 0


if __name__ == '__main__':
    spark = get_spark_session()
    spark.udf.register("length", length, IntegerType())
    spark.sql("select sum(length(ip)),sum(length(language)) from test.wrk_cdb_inc_product_on_hdfs").show(1, False)
