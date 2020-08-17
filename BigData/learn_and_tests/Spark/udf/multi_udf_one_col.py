# -*- coding:utf-8 -*-
"""
:Description: Spark SQL 多个UDF作用于一列
:Owner: jiajing_qu
:Create time: 2020/08/17 10:17
"""
from pyspark.sql import SparkSession

from pyspark.sql.types import IntegerType
from pyspark.sql.functions import udf, struct
from pyspark.sql.functions import lit
from pyspark.sql.functions import *


class udfs:
    def sum2(self, x):
        return x + 4

    def multi(self, x):
        return x * 2

    def div(self, x):
        return x / 3


fun_list = ["sum2", "multi", "div"]
udfs = udfs()


def my_udf(func_list):
    def all_udf(v):
        r = None
        for f in func_list:
            if r is None:
                r = getattr(udfs, f)(v)
            else:
                r = getattr(udfs, f)(r)
        return r
    return udf(all_udf, IntegerType())


def main():
    spark = SparkSession.builder.enableHiveSupport()\
        .config("hive.exec.dynamic.partition", True)\
        .config("hive.exec.dynamic.partition", True)\
        .config("hive.exec.dynamic.partition.mode", "nonstrict")\
        .appName("Test udf").getOrCreate()

    df = spark.createDataFrame([(101, 1, 16)], ['ID', 'A', 'B'])
    df.show()

    df.withColumn('Result2', my_udf(fun_list)("A")).show()


if __name__ == "__main__":
    main()