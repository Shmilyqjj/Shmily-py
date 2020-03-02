#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 通过mongo的schema生成spark的schema
:Author: jiajing_qu
:Create Time: 2020/2/29 20:24
:File: generate_spark_schema_json_by_mongo_schema
:Site: shmily-qjj.top
"""
from pyspark.sql.functions import udf, when, size, col
from pyspark.sql.types import StructType, LongType
import time

try:
    import MySQLdb
    import MySQLdb.cursors
except ImportError:
    import pymysql as MySQLdb

import json
import re
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MYSQL_DB='sql_test'
MYSQL_TB='mongo_table_schema_mapping'
MYSQL_HOST='localhost'
MYSQL_USER='root'
MYSQL_PORT=3306
MYSQL_PWD='123456'

# DB SQL
"""
/*
 Navicat Premium Data Transfer

 Source Server         : Mysql-root
 Source Server Type    : MySQL
 Source Server Version : 80015
 Source Host           : localhost:3306
 Source Schema         : sql_test

 Target Server Type    : MySQL
 Target Server Version : 80015
 File Encoding         : 65001

 Date: 01/03/2020 00:23:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for mongo_table_schema_mapping
-- ----------------------------
DROP TABLE IF EXISTS `mongo_table_schema_mapping`;
CREATE TABLE `mongo_table_schema_mapping`  (
  `mongo_table` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mongo_schema` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`mongo_table`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mongo_table_schema_mapping
-- ----------------------------
INSERT INTO `mongo_table_schema_mapping` VALUES ('test_table', '{\r\n    name: { type: String },\r\n    login_accounts: [{\r\n        union_id: { type: String },\r\n        open_id: { type: String },\r\n        account_type: { type: String },\r\n        created_time: { type: Date }\r\n    }],\r\n    sensitive_name: { type: String },\r\n    union_id: { type: String }, // ？\r\n    area_code: { type: String },\r\n    account: { type: String }, // 帐号，手机号\r\n    password: { type: String },\r\n    photo_url: { type: String },\r\n    big_photo_url: { type: String },\r\n    photo: { type: Buffer },\r\n    image_type: { type: String },\r\n    email: { type: String },\r\n    title: { type: String }, // 职位\r\n    domain: { type: String }, // 行业\r\n    openid: { type: String }, // 微信open_id\r\n    mobile: { type: String },\r\n    registration_spread_code: { type: String },\r\n    qq: { type: String },\r\n    fax: { type: String }, // 传真\r\n    platform: { type: String }, // 账号注册平台\r\n    contact: { type: String },\r\n    company: { type: String },\r\n    eid: { type: String },\r\n    department: { type: String },\r\n    evaluated_enterprises: [\r\n        {\r\n            name: { type: String },\r\n            eid: { type: String }\r\n        }\r\n    ],\r\n    usercollects: [\r\n        {\r\n            name: { type: String },\r\n            eid: { type: String },\r\n            item: { type: mongoose.Schema.Types.ObjectId, ref: \'usercollects\' }\r\n        }\r\n    ],\r\n    addresses: [\r\n        {\r\n            name: { type: String },\r\n            post_code: { type: String },\r\n            address: { type: String },\r\n            telephone: { type: String },\r\n            is_default: { type: String }\r\n        }\r\n    ],\r\n    login_devices: [\r\n        {\r\n            device_id: { type: String },\r\n            registration_id: { type: String },\r\n            platform: { type: String },\r\n            is_active: { type: Number },\r\n            login_time: { type: Date, default: Date.now },\r\n            app_version: { type: String }\r\n        }\r\n    ],\r\n    login_type: { type: String },\r\n    suggestions: [{ type: mongoose.Schema.Types.ObjectId, ref: \'suggestions\' }],\r\n    agent: { type: String }, // 中介代理：默认是QXB\r\n    level: { type: String }, // 会员等级\r\n    qxb_balance: { type: Number }, // 启信币余额\r\n    points: { type: Number }, // 会员积分\r\n    last_login_app: { type: Date }, // 最后app登录日期\r\n    last_login_web: { type: Date }, // 最后web登录日期\r\n    last_login_weixin: { type: Date }, // 最后weixin登录日期\r\n    last_updated_time: { type: Date },\r\n    created_time: { type: Date },\r\n    is_fee_reminder: [{ biz_type: { type: String }, is_reminder: { type: String } }], // 收费提醒：{业务类型，是否提醒}  Y/N\r\n    decision_report_mail: { type: String },\r\n    decision_report_mobile: { type: String },\r\n    uid: { type: String },\r\n    profile: { type: mongoose.Schema.Types.ObjectId, ref: \'userprofiles\' },\r\n    article_ids: [{ type: String }],\r\n    customize_app: [{ type: String }],\r\n    myapp_customize: [{ type: String }], // 首页应用定制\r\n    myapp_customize_new: { type: String }, // 4.7.1版本之后首页应用定制\r\n    myapp_customize_new_600: { type: String }, // 6.0.0版本之后首页应用定制\r\n    associationCustomize_app: [{ type: String }], // 社团接口定制\r\n    lawFirmCustomize_app: [{ type: String }], // 律所接口定制\r\n    hkCustomize_app: [{ type: String }], // 香港企业接口定制\r\n    grade: { type: Number },\r\n    vip_start_date: { type: Date },\r\n    vip_expired_date: { type: Date },\r\n    channel_id: { type: String },\r\n    app_settings: {\r\n        monitor: {\r\n            disable_push: { type: Boolean },\r\n            sync_to_business: { type: Boolean },\r\n            sync_time: { type: Date },\r\n            disable_message: { type: Boolean },\r\n            rec_message_mobile: { type: String },\r\n            disable_email: { type: Boolean },\r\n            rec_email_address: { type: String }\r\n        },\r\n        push: {\r\n            items: [{ type: String }]\r\n        }\r\n    },\r\n    monitor_enterprises: [{\r\n        eid: { type: String },\r\n        name: { type: String },\r\n        entity_type: { type: Number },\r\n        start_time: { type: Date },\r\n        expired_time: { type: Date }\r\n    }],\r\n    user_collect_version: { type: Number, default: 0 },\r\n    default_groups_generated: { type: Number },\r\n    rebate_number: { type: Number }, // 报告抵用券的数量\r\n    vip_mobile: { type: String },\r\n    vip_card_number: { type: String },\r\n    free_vip_type: { type: Number },\r\n    packages: [{ code: { type: String } }],\r\n    package: { type: String },\r\n    b_end_date: { type: Date },\r\n    upgrade_reminder: { type: Number }, // APP升降级提示，1升级需提示，2升级已提示+降级需提示，3降级已提示\r\n    pwdbak: { type: String },\r\n    source: { type: String },\r\n    real_name: { type: String },//用户真实姓名\r\n    claim_ent: { type: String },//用户认证的企业\r\n    claim_eid: { type: String },//用户认证企业id\r\n    login_channel: { type: String },//登录时渠道\r\n    login_version: { type: String },//登录时版本\r\n    user_type: [{ type: String }],\r\n    ip: { type: String },\r\n    is_spider: { type: Boolean }\r\n}');
INSERT INTO `mongo_table_schema_mapping` VALUES ('test_table1', '{}');

SET FOREIGN_KEY_CHECKS = 1;
"""

# mongo与spark的数据类型映射
mongo_spark_type_mapping = {
    # mongo type: spark type
    "String": "string",
    "Date": "timestamp",
    "Number": "long",
    "Boolean": "boolean",
    "mongoose.Schema.Types.ObjectId": "string",
}


def trans_json(json_str):
    """
    给json内的键和值加上双引号
    :param json_str: 键值无双引号的json字符串
    :return: 转换好的json字符串 可以供eval或json.loads直接使用
    """
    json_str = json_str.replace("'", "").replace(" ", "").replace('\r', '').replace('"', '')
    need_replace = re.findall("[A-Za-z0-9_.]+", json_str)
    need_replace = set(need_replace)
    # need_replace = sorted(need_replace,key = lambda i:len(i),reverse=False)
    # print(need_replace)
    lines_list = json_str.split('\n')
    result_str = ''
    for line in lines_list:
        word_list = re.findall("[A-Za-z0-9_.]+", line)
        if word_list:
            for word in word_list:
                if word in need_replace and word != 'type':
                    line = re.sub(word+':', '"%s":' % word, line, count=1)
                    line = re.sub(':'+word, ':"%s"' % word, line, count=1)
                else:
                    line = line.replace('type:', '"type":')
        result_str += line + '\n'
    return result_str


# def trans_json(json_str):
#     """
#     [不支持python2]
#     给键值加双引号
#     参考网上资料说demjsob可以解决这种问题
#     但不清楚机器能不能装，尽量不装吧。。自己解析。。
#     https://github.com/dmeranda/demjson, 速度比标准库要慢。
#     :param json_str:
#     :return:
#     """
#     quote_pat = re.compile(r'".*?"')
#     a = quote_pat.findall(json_str)
#     json_str = quote_pat.sub('@', json_str)
#     key_pat = re.compile(r'(\w+):')
#     json_str = key_pat.sub(r'"\1":', json_str)
#     assert json_str.count('@') == len(a)
#     count = -1
#     def put_back_values(match):
#         count = -1
#         count += 1
#         return a[count]
#     json_str = re.sub('@', put_back_values, json_str)
#     return json_str


def get_mongo_schema_in_db(table_name):
    """
    根据mongo表名 在数据库中获取到
    :param table_name:
    :return:
    """
    res = None
    try:
        conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PWD, db=MYSQL_DB)
        cur = conn.cursor()
        cur.execute("select mongo_schema from %s where mongo_table= '%s'" % (MYSQL_TB, table_name))
        res = cur.fetchall()
    except Exception as e:
        logger.error(e)
    finally:
        cur.close()
        conn.close()
    if res:
            schema_str = res[0][0]
            schema_str = re.sub("//[\s\S]*?\n", "\n", schema_str)  # 去掉schema上的注释
            schema_str = trans_json(schema_str)  # 对 不合法的k v 进行转换  添加引号
            # print(schema_str)
            schema_json = {}
            try:
                schema_json = eval(schema_str)
            except Exception as e:
                logger.error("请检查Json格式是否正确  %s" % e)
            logger.debug(schema_json)
            return schema_json
    else:
            logger.warn("未在数据库中找到表%s的schema信息")
            return {}


def mongo_schema_to_spark_schema(mongo_schema_json):
    """
    Mongo schema json 转 Spark可以读取的schema (df.schema.json()形式)
    :param mongo_schema_json: mongo的schema    <class:dict>
    :return:  spark.read.format("com.mongodb.spark.sql").options(**config).load(schema=StructType.fromJson(schema_json)) 中的table_name: schema_json
    schema_json格式 大概：
        {'fields': [{'metadata': {},
       'name': '_id',
       'nullable': True,
       'type': {'fields': [{'metadata': {},
          'name': 'oid',
          'nullable': True,
          'type': 'string'}],
        'type': 'struct'}},
      {'metadata': {}, 'name': 'check_result', 'nullable': True, 'type': 'string'},
      {'metadata': {}, 'name': 'dps_token', 'nullable': True, 'type': 'string'},
      {'metadata': {}, 'name': 'image_name', 'nullable': True, 'type': 'string'},
      {'metadata': {},
       'name': 'image_name_dps',
       'nullable': True,
       'type': 'string'},
      {'metadata': {}, 'name': 'match_type', 'nullable': True, 'type': 'string'},
      {'metadata': {}, 'name': 'name_space', 'nullable': True, 'type': 'string'},
      {'metadata': {}, 'name': 'ocr', 'nullable': True, 'type': 'string'},
      {'metadata': {}, 'name': 'ori_label', 'nullable': True, 'type': 'string'},
      {'metadata': {}, 'name': 'server_type', 'nullable': True, 'type': 'string'},
      {'metadata': {}, 'name': 'task_token', 'nullable': True, 'type': 'string'},
      {'metadata': {}, 'name': 'time_create', 'nullable': True, 'type': 'string'},
      {'metadata': {}, 'name': 'token', 'nullable': True, 'type': 'string'}],
     'type': 'struct'},

    """
    field_info_list = []
    # __v和_id问题
    field_info_list.append({'metadata': {}, 'name': '__v', 'nullable': True, 'type': 'long'})
    # field_info_list.append({'metadata': {}, 'name': '_id', 'nullable': True, 'type': 'string'})
    field_info_list.append({'metadata': {},
           'name': '_id',
           'nullable': True,
           'type': {'fields': [{'metadata': {},
              'name': 'oid',
              'nullable': True,
              'type': 'string'}],
            'type': 'struct'}})

    for field in mongo_schema_json:
        field_info = mongo_schema_json[field]
        if isinstance(field_info, dict):
            spark_data_type = mongo_spark_type_mapping.get(field_info.get('type')) if mongo_spark_type_mapping.get(field_info.get('type')) else 'string'
            field_info_list.append({'metadata': {}, 'name': field, 'nullable': True, 'type': spark_data_type})
        elif isinstance(field_info, list):
            print(field)
            print(field_info)
            print(len(field_info))
            second_info_dict = {'fields':[], 'type': 'struct'}
            # field_info  [{'type': 'String'}] or [{'eid': {'type': 'String'}, 'name': {'type': 'String'}, 'entity_type': {'type': 'Number'}, 'start_time': {'type': 'Date'}, 'expired_time': {'type': 'Date'}}]
            for second_field_dict in field_info:  # 一般这个list只含有一个dict
                if second_field_dict.get('type'):  # field是article_ids  second_field_dict是{'type': 'String'}
                    mongo_type = second_field_dict.get('type')
                    spark_type = mongo_spark_type_mapping.get(mongo_type) if mongo_spark_type_mapping.get(mongo_type) else 'string'
                    second_info_dict.get('fields').append(
                        {'containsNull': True, 'elementType': spark_type, 'type': 'array'})
                else:
                    print(second_field_dict)  # field是is_fee_reminder  second_field_dict是{'biz_type': {'type': 'String'}, 'is_reminder': {'type': 'String'}}
                    for second_field in second_field_dict:
                        second_field_info = second_field_dict[second_field]
                        mongo_type = second_field_info.get('type')
                        spark_type = mongo_spark_type_mapping.get(mongo_type) if mongo_spark_type_mapping.get(
                            mongo_type) else 'string'
                        second_info_dict.get('fields').append({'metadata': {}, 'name': second_field, 'nullable': True, 'type': spark_type})
            field_info_list.append({'metadata': {},
                                    'name': field,
                                    'nullable': True,
                                    'type': {
                                        'containsNull': True,
                                        'elementType': second_info_dict,
                                        'type': 'array'}
                                    })
        # {'metadata': {}, 'name': '__v', 'nullable': True, 'type': 'long'}
    schema = {'fields': field_info_list,
              'type': 'struct'}
    return schema


def generate_mongo_spark_schema(spark, mongo_ip, mongo_port, mongo_user, mongo_password,mongo_table, partitions = 1000):
    """
    通过spark 推断mongo的schema
    :param spark: spark
    :param mongo_ip: ip
    :param mongo_port:  port
    :param mongo_user: user
    :param mongo_password: pwd
    :param mongo_table:  mongo表名
    :param partitions:  通过partitions个分区数 对schema进行推断 默认1000个分区
    :return: schema json
    """
    def cast_mongo_timestamp(time_col):
        """
        UDF
        mongo 的timestamp 转成 13位精确的时间戳，mongo的时间都是utc时间
        如果要得到当前的时间，需要 +8小时，但因为历史原因都没有+8小时
        所以mongo到hive的时间都是utc时间，不要轻易改
        :param time_col:
        :return:
        """
        # t = datetime.datetime.strptime(time_col,"%Y-%m-%d %H:%M:%S.%f")
        # time_col 传进来就是 datetime.datetime 格式的，所以不需要转换
        try:
            if not time_col:
                return None
            t = time_col
            ti = t.timetuple()
            timeStamp = int(time.mktime(ti))
            return int((str(timeStamp) + str("%03d" % t.microsecond))[:13])
        except:
            return int(0)
    def mongo_castBinaryToString(df):
        """
        转换mysql的binary类型为string类型
        withcolumn 会先判断df是否有该字段，有就在原字段基础上改
        :param df：
        """
        for col_name, col_type in df.dtypes:
            if col_type == "binary":
                df = df.withColumn(col_name, getattr(df, col_name).cast("string"))
            if col_type == "timestamp":
                cast_mongo_timestamp_udf = udf(cast_mongo_timestamp, LongType())
                df = df.withColumn(col_name, cast_mongo_timestamp_udf(col_name))
            if col_type.startswith("array"):
                df = df.withColumn(col_name, when(size(col(col_name)) == 0, None).otherwise(col(col_name)))
        return df
    uri = "mongodb://'{mongo_user}':{mongo_password}@{mongo_ip}:{mongo_port}/{mongo_table}".format(
    mongo_user=mongo_user,mongo_password=mongo_password, mongo_ip=mongo_ip, mongo_port=mongo_port, mongo_table=mongo_table)
    config = {}
    config.update({"uri": uri})
    config.update({
        "spark.mongodb.input.partitioner": "MongoPaginateByCountPartitioner",
        "spark.mongodb.input.partitionerOptions.partitionKey": "_id",
        "spark.mongodb.input.partitionerOptions.numberOfPartitions": "%d" % partitions,
        "spark.mongodb.input.readPreference.name": "secondaryPreferred"
    })
    data = spark.read.format("com.mongodb.spark.sql").options(**config).load()
    data = mongo_castBinaryToString(data)
    schema = data.schema.json()
    return schema


if __name__ == '__main__':
    mongo_schema_json = get_mongo_schema_in_db("test_table")
    print(mongo_schema_json)
    schema = mongo_schema_to_spark_schema(mongo_schema_json)
    print(schema)