#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description:
:Owner: jiajing_qu
:Create time: 2019/9/23 11:58
"""
from tesla.base_data.behavior.streaming import base_cdb_streaming
from pyspark.sql.functions import col, size, when
from tesla.common.utility.para_deal import auto_batch
from tesla.common.utility.sparkUtils.base_spark import Base_Spark
TOPICS = "cloud_behavior_other,cloud_behavior,cloud_behavior_qxb,cloud_behavior_cc,cloud_behavior_cs,cloud_behavior_zdao"


def cdbp2hive(spark, topics):
    """
    :desc: cdbp数据存入hive
    :param spark:
    :param topics:
    :return:
    """
    cdb_df = base_cdb_streaming.get_cdbDF(spark, topics, config={}, env="ONLINE")
    cdb_df = cdb_df.withColumn('targets', when(size(col('targets')) == 0, None).otherwise(col('targets'))) \
        .withColumn('other_para', when(size(col('other_para')) == 0, None).otherwise(col('other_para')))

    cdb_df = cdb_df.filter(
            "ip is null or (lower(product_name) not rlike '(^camcard)|(^camscanner)|(^ccb)|(^companyinfo)|(^ecard)|(^leads_builder)|(^qxb)|(^zdao)|(^zhaobiao)|(^zaodao)' or lower(product_name)=='zdao_qiye' )  or ip != '101.95.128.162'")
    cdb_df.registerTempTable("cdb_tmp_table")
    sql = ('''
              select *,case when operation in ('send_sms','sent_sms','delivered_sms','unsubscribe_sms') then 'other_sms'
              when lower(product_name) like 'camcard%'   or lower(product_name) in ('ecard','companyinfo') then 'cc'
              when lower(product_name) like 'camscanner%' then 'cs'
              when lower(product_name) in ('bs','zdao', 'bs_mobile', 'zdao_zhaopin') or lower(product_name) like 'zaodao%' then 'zdao'
              when lower(product_name) like 'qxb%' or lower(product_name) like '%qixinbao' then 'qxb'
              when lower(substr(product_name,1,3)) = 'zp_' then 'zp'
              else 'other' end product ,
              concat(
              from_unixtime(unix_timestamp() +4*60 , 'yyyyMMdd0005')
               ,'_'
               ,from_unixtime(unix_timestamp()+3600*24 +4*60 , 'yyyyMMdd0005')
              ) batch
              from cdb_tmp_table
        ''')

    cdb_df = spark.sql(sql)
    # checkpoint
    checkpoint_location = '/data_test/kafka_checkpoint/cdbp2hive_checkpoint/' + topics.replace(',', '_')

    # 数据存放地址
    data_path = "/user/hive/warehouse/test.db/wrk_cdb_inc_product"
    # 以parquet格式按"batch", "product", "operation"这三个字段进行分区
    query = cdb_df.writeStream\
          .outputMode("append")\
          .format("parquet")\
          .option("checkpointLocation", checkpoint_location) \
          .option("path", data_path) \
          .partitionBy("batch", "product", "operation") \
          .trigger(processingTime='60 seconds') \
          .start()
    query.awaitTermination()


def main(spark):
    cdbp2hive(spark, TOPICS)


if __name__ == '__main__':
    spark_config = {
        "hive.exec.dynamic.partition": "true",
        "hive.exec.dynamic.partition.mode": "nonstrict",
        "spark.yarn.executor.memoryOverhead": "10240",
        "spark.sql.shuffle.partitions": "1000",
    }
    spark = Base_Spark('cdbp2hive_streaming', config=spark_config)
    main(spark)