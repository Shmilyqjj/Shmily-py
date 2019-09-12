#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: Spark + Python 学习  pySpark
:Owner: jiajing_qu
:Create time: 2019/9/10 14:26
"""

"""
原理部分:
shuffle 是划分 DAG 中 stage 的标识,同时影响 Spark 执行速度的关键步骤
窄依赖跟宽依赖的区别是是否发生 shuffle(洗牌) 操作.宽依赖会发生 shuffle 操作. 窄依赖是子 RDD的各个分片(partition)不依赖于其他分片,能够独立计算得到结果
宽依赖指子 RDD 的各个分片会依赖于父RDD 的多个分片,所以会造成父 RDD 的各个分片在集群中重新分片。
map就是一种窄依赖，而join则会导致宽依赖
map,filter,union属于第一类窄依赖，而join with inputs co-partitioned（对输入进行协同划分的join操作，也就是说先按照key分组然后shuffle write的时候一个父分区对应一个子分区）则为第二类窄依赖
groupByKey和对输入未协同划分的join操作就是宽依赖，这是shuffle类操作。
shuffle 操作是 spark 中最耗时的操作,应尽量避免不必要的 shuffle.


"""




"""
pyspark - core

sc:
class pyspark.SparkContext（master = None，appName = None，sparkHome = None，pyFiles = None，environment = None，batchSize = 0，serializer = PickleSerializer（），conf = None，gateway = None，jsc = None，profiler_cls = <class'pyspark .profiler.BasicProfiler'> 

SparkContext不支持实例跨多个进程共享，并且PySpark不保证多处理执行。使用线程代替并发处理。


spark conf:
class pyspark.SparkConf（loadDefaults = True，_jvm = None，_jconf = None ）
对于单元测试，您也可以调用SparkConf(false)以跳过加载外部设置并获得相同的配置，无论系统属性如何。

coalesce()和repartition():
repartition只是coalesce接口中shuffle为true的简易实现，（假设RDD有N个分区，需要重新划分成M个分区） 
N < M 一般情况下N个分区有数据分布不均匀的状况，利用HashPartitioner函数将数据重新分区为M个，这时需要将shuffle设置为true。 
N > M并且N和M相差不多，(假如N是1000，M是100)那么就可以将N个分区中的若干个分区合并成一个新的分区，最终合并为M个分区，这时可以将shuff设置为false，在shuffl为false的情况下，如果M>N时，coalesce为无效的，不进行shuffle过程，父RDD和子RDD之间是窄依赖关系。 
N > M并且两者相差悬殊，这时如果将shuffle设置为false，父子RDD是窄依赖关系，他们同处在一个stage中，就可能造成Spark程序的并行度不够，从而影响性能，如果在M为1的时候，为了使coalesce之前的操作有更好的并行度，可以讲shuffle设置为true


"""

"""
pyspark - sql

Spark SQL和DataFrames的重要类：
pyspark.sql.SparkSessionDataFrameSQL功能的 主要入口点。
pyspark.sql.DataFrame 分布在命名列中的分布式数据集合。
pyspark.sql.Column 一个列中的列表达式DataFrame。
pyspark.sql.Row 一行中的数据DataFrame。
pyspark.sql.GroupedData 聚合方法，由返回DataFrame.groupBy()。
pyspark.sql.DataFrameNaFunctions 处理缺失数据的方法（空值）。
pyspark.sql.DataFrameStatFunctions 统计功能的方法。
pyspark.sql.functions 可用的内置函数列表DataFrame。
pyspark.sql.types 可用的数据类型列表。
pyspark.sql.Window 用于处理窗口功能。

class pyspark.sql.SparkSession（sparkContext，jsparkSession = None ）

df = spark.sql

"""

"""
性能优化:

"""