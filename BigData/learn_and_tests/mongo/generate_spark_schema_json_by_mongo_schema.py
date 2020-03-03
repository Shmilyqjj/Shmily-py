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
import platform

try:
    import MySQLdb
    import MySQLdb.cursors
except ImportError:
    import pymysql as MySQLdb

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
    "mongoose.Schema.Types.ObjectId": "string",  # 这个必须开头 顺序不能变
    "String": "string",
    "Date": "timestamp",
    "Number": "long",
    "Boolean": "boolean",
}
spark_mongo_type_mapping = {v:k for k, v in mongo_spark_type_mapping.items()}
# spark_mongo_type_mapping.update({'array<string>': 'String'})


def delete_comment(mongo_schema_str):
    """
    去掉 mongo schema上的注释
    :param mongo_schema_str:
    :return:
    """
    return re.sub("//[\s\S]*?\n", "\n", mongo_schema_str)  # 去掉schema上的注释


def trans_json(json_str):
    """
    给json内的键和值加上双引号
    :param json_str: 键值无双引号的json字符串
    :return: 转换好的json字符串 可以供eval或json.loads直接使用
    """
    json_str = json_str.replace("'", "").replace(" ", "").replace('"', '')
    need_replace = re.findall("[A-Za-z0-9_.]+", json_str)
    need_replace = set(need_replace)
    # need_replace = sorted(need_replace,key = lambda i:len(i),reverse=False)
    # print(need_replace)
    sys_name = platform.system()
    if sys_name == 'Windows':
        split_str = '\r\n'
    else:
        split_str = '\n'
    lines_list = json_str.split(split_str) # linux里 \n    win里 \r\n
    result_str = ''
    for line in lines_list:
        word_list = re.findall("[A-Za-z0-9_.]+", line)
        if word_list:
            for word in word_list:
                if word in need_replace and word != 'type':
                    line = re.sub(word+':', '"%s":' % word, line, count=1)
                    line = re.sub(':'+word, ':"%s"' % word, line, count=1)
                else:
                    line = line.replace('type:', '"type":') if len(re.findall(r"(type)", line)) == 1 else\
                    re.sub("[^_](type):", '{"type":', line, count=1)

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


def check_mongo_schema(mongo_schema_str):
    """
    检查mongo schema是否合理
    :param: mongo_schema_str
    :return: True / Error Info
    """
    logger.info("开始检查输入的schema格式是否正确")
    try:
        tmp = delete_comment(mongo_schema_str)
        json_str = trans_json(tmp)
        # print(json_str)  # json_str带双引号的
        import json
        json.loads(json_str)
        # eval(json_str)  # eval看不到错误信息
        logger.info("schema格式正确")
        return True
    except Exception as e:
        logger.error("schema格式错误")
        return e


def mysql_interface(sql):
    """
    统一mysql入口
    :param sql:  sql语句
    :return:  fetchall的结果
    """
    try:
        conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PWD, db=MYSQL_DB)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        result = cur.fetchall()
        return result
    except Exception as e:
        logger.error(e)
    finally:
        cur.close()
        conn.close()


def get_mongo_schema_in_db(table_name):
    """
    根据mongo表名 在数据库中获取到
    :param table_name:
    :return:
    """
    sql = "select mongo_schema from %s where mongo_table= '%s'" % (MYSQL_TB, table_name)
    res = mysql_interface(sql)
    if res:
            schema_str = res[0][0]
            schema_str = delete_comment(schema_str)
            schema_str = trans_json(schema_str)  # 对 不合法的k v 进行转换  添加引号
            schema_json = {}
            try:
                import json
                schema_json = json.loads(schema_str)
                # schema_json = eval(schema_str)
            except Exception as e:
                logger.error(schema_str)
                logger.error("请检查Json格式是否正确(可能是Json转换出现问题)  %s" % e)
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
            # field_info  [{'type': 'String'}] or [{'eid': {'type': 'String'}, 'name': {'type': 'String'}, 'entity_type': {'type': 'Number'}, 'start_time': {'type': 'Date'}, 'expired_time': {'type': 'Date'}}]
            if len(field_info[0]) == 1 or ('type' in field_info[0] and 'ref' in field_info[0]):  # 一般这个list只含有一个dict
                mongo_type = field_info[0].get('type')
                spark_type = mongo_spark_type_mapping.get(mongo_type) if mongo_spark_type_mapping.get(mongo_type) else 'string'
                second_info_dict = spark_type
                # print(field_info)
            else:
                second_info_dict = {'fields': [], 'type': 'struct'}
                second_field_dict = field_info[0]  # 一般这个list只含有一个dict
                # print(second_field_dict)  # field是is_fee_reminder  second_field_dict是{'biz_type': {'type': 'String'}, 'is_reminder': {'type': 'String'}}
                for second_field in second_field_dict:
                    second_field_info = second_field_dict[second_field]
                    mongo_type = second_field_info.get('type')
                    spark_type = mongo_spark_type_mapping.get(mongo_type) if mongo_spark_type_mapping.get(mongo_type) else 'string'
                    # print(second_field)
                    # print(second_field_info)
                    second_info_dict.get('fields').append({'metadata': {}, 'name': second_field, 'nullable': True, 'type': spark_type})
            field_info_list.append({'metadata': {},
                                    'name': field,
                                    'nullable': True,
                                    'type': {
                                        'containsNull': True,
                                        'elementType': second_info_dict,
                                        'type': 'array'}
                                    })
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


def show(spark_schema_json):
    """
    从spark的schema json解析 字段：类型  直观显示(可以展示为树形结构 类似linux tree命令的结果)
    用于给前端页面显示的结果
    :param spark_schema_json:
    :return: dict
    """
    field_info_list = spark_schema_json['fields']
    result_dict = {}
    for i in field_info_list:
        # i有几种形式
        # {'metadata': {}, 'name': 'app_settings', 'nullable': True, 'type': 'string'}
        # {'metadata': {},'name': '_id','nullable': True,'type': {'fields': [{'metadata': {},'name': 'oid','nullable': True,'type': 'string'}],'type': 'struct'}}
        # {'metadata': {}, 'name': 'packages', 'nullable': True, 'type': {'containsNull': True, 'elementType': {'fields': [{'metadata': {}, 'name': 'code', 'nullable': True, 'type': 'string'}], 'type': 'struct'}, 'type': 'array'}}
        # {'metadata': {}, 'name': 'packages', 'nullable': True, 'type': {'containsNull': True, 'elementType': 'string', 'type': 'array'}}
        first_type = i.get('type')
        first_name = i.get('name')
        if isinstance(first_type, str):
            result_dict[first_name] = {'type': first_type, 'children' :{}}  # 没有第二级字段
        elif isinstance(first_type, dict) and isinstance(first_type.get('elementType'), str):
            first_type = first_type.get('elementType')
            result_dict[first_name] = {'type': "array<%s>" % first_type, 'children' :{}}  # 没有第二级字段
        elif first_type.get('fields') and isinstance(first_type.get('fields'), list):
            # 这层 只会有_id.oid进来
            second_name = first_type.get('fields')[0].get('name')
            second_type = first_type.get('fields')[0].get('type')
            result_dict[first_name] = {'type': "struct<%s:%s>" % (second_name, second_type), 'children' :{second_name: second_type}}
        else:
            # [{'metadata': {}, 'name': 'name', 'nullable': True, 'type': 'string'}, {'metadata': {}, 'name': 'eid', 'nullable': True, 'type': 'string'}]
            fields_list = first_type.get('elementType').get('fields')
            field_type = first_type.get('elementType').get('type')  # array or struct
            internal_type_list = []
            children_dict = {}
            for info in fields_list:
                second_name = info.get('name')
                second_type = info.get('type')
                internal_type_list.append('%s:%s' % (second_name, second_type))
                children_dict[second_name] = second_type
            result_dict[first_name] = {'type': '%s<%s>' % (field_type, ','.join(internal_type_list)), 'children': children_dict}
    return result_dict


def add_and_update_mongo_spark_schema(add_schema_json):
    """
    对已有的schema进行更新(添加字段)  add_schema_json转成mongo的schema并提交更新至数据库
    :param add_schema_json: 与show查询出来的格式一样  如果更新 在已有基础上更新
    :return:True 更新成功  exception更新失败
    """
    new_mongo_schema_str_list = []
    new_mongo_schema = {}
    for first_field in add_schema_json:
        first_field_info = add_schema_json[first_field] # {'type': 'long', 'children': {}} or {'type': 'struct<oid:string>', 'children': {'oid': 'string'}}
        children = first_field_info.get('children')
        if first_field == '__v' or first_field == '_id':
            pass
        elif children == {}:
            first_field_type = first_field_info.get('type') if first_field_info.get('type') else 'string'
            if first_field_type == 'array<string>':
                mongo_v = [{'type': 'String'}]
                new_mongo_schema[first_field] = mongo_v
                new_mongo_schema_str_list.append('%s:[\n{type : String}\n],' % first_field)
            else:
                mongo_type = spark_mongo_type_mapping.get(first_field_type)
                new_mongo_schema[first_field] = {'type': mongo_type}
                new_mongo_schema_str_list.append('%s:{ type : %s },' % (first_field, mongo_type))
        else:
            second_field_list = []
            second_field_str_list = []
            second_field_dict = {}
            for second_field in children:

                if second_field == '__v' or second_field == '_id':
                    pass
                else:
                    second_field_type = children[second_field]
                    # print(second_field_type)
                    mongo_type = spark_mongo_type_mapping.get(second_field_type) if spark_mongo_type_mapping.get(second_field_type) else 'string'
                    second_field_dict.update({second_field: {'type': mongo_type}})
                    second_field_str_list.append("%s: {type: %s}," % (second_field, mongo_type))
            second_field_list.append(second_field_dict)
            second_field_str = '[\n{' + '\n'.join(second_field_str_list).rstrip(',') + '}\n]'
            new_mongo_schema[first_field] = second_field_list
            new_mongo_schema_str_list.append('%s: %s,' % (first_field, second_field_str))
    new_mongo_schema_str = '{' + '\n'.join(new_mongo_schema_str_list).rstrip(',') + '}'
    # new_mongo_schema_str = MySQLdb.escape_string(new_mongo_schema_str)
    # sql = """insert into mongo_table_schema_mapping(mongo_table,mongo_schema) values ('final3',"%s")""" % new_mongo_schema
    # print(sql)
    # mysql_interface(sql)
    return new_mongo_schema_str, new_mongo_schema


if __name__ == '__main__':
    mongo_schema_json = get_mongo_schema_in_db("test_table")
    print(1, str(mongo_schema_json))
    schema = mongo_schema_to_spark_schema(mongo_schema_json)
    print(2, schema)
    res = show(schema)
    print(3, res)
    new_mongo_schema_str, new_mongo_schema = add_and_update_mongo_spark_schema(res)
    print(check_mongo_schema(new_mongo_schema_str))
    print(new_mongo_schema_str)
    # print(trans_json(delete_comment(new)))
    print(check_mongo_schema(new_mongo_schema_str))
    # mongo_schema_to_spark_schema(new)

