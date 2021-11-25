#!/usr/bin/env python
# encoding: utf-8
"""
:Author: shmily
:Create Time: 2021/10/30 下午12:44
:@File: mysql_interface.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""
import time
import traceback
import logging

try:
    import MySQLdb
    import MySQLdb.cursors
except ImportError:
    import pymysql as MySQLdb
from Python_Applications.python_web.flask_app.conf.config import config
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MysqlInterface(object):
    """
    Mysql 公共类
    """
    def __new__(cls, *args, **kwargs):
        # Singleton
        if not hasattr(cls, "_instance"):
            cls._instance = super(MysqlInterface, cls).__new__(cls)
        return cls._instance

    def __init__(self, ip=None, port=None, user=None, password=None, db_name=None, charset='utf8', connect_timeout=8):
        """
        初始化  获取mysql的连接信息
        :param ip:
        :param port:
        :param user:
        """
        self.ip = ip if ip else config.get("db").DATABASE_IP
        self.port = int(port) if port else int(config.get("db").DATABASE_PORT)
        self.user = user if user else config.get("db").DATABASE_USER
        self.password = str(password) if password else config.get("db").DATABASE_PWD
        self.charset = charset
        self.connect_timeout = connect_timeout
        self.db_name = db_name if db_name else config.get("db").DATABASE_NAME

    def get_conn_info(self):
        return {"ip": self.ip, "port": self.port, "user": self.user, "password": self.password, "charset": self.charset,
                "connect_timeout": self.connect_timeout}

    def get_conn_link(self):
        return "jdbc:mysql://%s:%s/%s?zeroDateTimeBehavior=convertToNull" % (self.ip, self.port, self.db_name)

    def get_table_fields_info(self, table_name):
        """
        获取Mysql表字段的信息
        :param table_name:
        :return:
        """
        sql = "SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s'" % (self.db_name, table_name)
        return self.query(sql)

    def get_table_data_count(self, table_name):
        """
        获取单表数据量
        :param table_name:
        :return:
        """
        sql = "SELECT count(1) FROM '%s'.'%s'" % (self.db_name, table_name)
        return self.query(sql)

    def get_connect(self):
        return MySQLdb.connect(host=self.ip,
                               user=self.user,
                               passwd=self.password,
                               port=self.port,
                               charset=self.charset,
                               connect_timeout=self.connect_timeout,
                               db=self.db_name,
                               cursorclass=MySQLdb.cursors.DictCursor)

    @staticmethod
    def escape(value):
        """
        对值进行转换 防止数据有问题
        :param value:
        :return:
        """
        value = value.replace('\\', '\\\\')
        value = value.replace('\'', '\\\'')
        return value

    def get_pd(self, sql):
        try:
            pd_df = pd.read_sql(sql, con=self.get_connect())
            return pd_df
        except:
            traceback.print_exc()
            return False

    def query(self, sql):
        """
        查  （查询数据）
        通用的对某个库进行查询sql的方法
        :param sql:  sql
        :return:
        """
        conn = None
        cursor = None
        start_time = time.time()
        try:
            conn = self.get_connect()
            cursor = conn.cursor()
            rows = cursor.execute(sql)
            results = cursor.fetchall()
            conn.commit()
            return {'rows': rows, 'fetch': results, 'duration': (time.time() - start_time)}
        except:
            traceback.print_exc()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def insert(self, table_name, data_dict, ignore=False):
        """
        增 （插入mysql）
        :param data_dict: Dict, insert value, eg:{column1: value1, column2: value2, ...}
        :param table_name: table name
        :param ignore: Bool, use IGNORE in sql or not
        :return: success return count of affect rows else return False
        """
        data_hash = data_dict.copy()
        insert_sql = "INSERT INTO " + table_name + " "
        if ignore:
            insert_sql = "INSERT IGNORE INTO " + table_name + " "
        sql_keys = ''
        sql_values = ''
        for data_key in data_hash.keys():
            if isinstance(data_hash[data_key], str):
                data_hash[data_key] = self.escape(str(data_hash[data_key]))
            else:
                if data_hash[data_key] is None:
                    data_hash[data_key] = ''
                data_hash[data_key] = str(data_hash.get(data_key))
            sql_keys += "`" + data_key + "`,"
            sql_values += "'" + data_hash[data_key] + "',"
        sql_keys = sql_keys[:-1]
        sql_values = sql_values[:-1]
        insert_sql += "(" + sql_keys + ") VALUES (" + sql_values + ")"
        logger.debug(insert_sql)
        result = self.query(insert_sql)
        return result.get('rows') if result else False

    def delete(self, table_name, condition=''):
        """
        删 （从mysql删除）
        :param table_name:  mysql table name
        :param condition:  条件 "where a = '1'"
        :return:
        """
        delete_sql = "delete from %s.%s %s" % (self.db_name, table_name, condition)
        logger.debug(delete_sql)
        return self.query(delete_sql)

    def update(self, table_name, data_dict, condition=None):
        """
        改  （更新数据）
        :param table_name: mysql table name
        :param data_dict: Dict, update columns, eg:{column1: value1, column2: value2, ...}
        :param condition: string, column used in WHERE Syntax, eg: "where eid <> 1 and name = 'qjj'"
        :return: success return count of affect rows else return False
        """
        data_hash = data_dict.copy()
        update_sql = "UPDATE `" + table_name + "` "
        if data_hash:
            update_sql += 'SET '
            for data_key in data_hash.keys():
                if isinstance(data_hash[data_key], str):
                    data_hash[data_key] = self.escape(data_hash[data_key])
                else:
                    if data_hash[data_key] is None:
                        data_hash[data_key] = ''
                    data_hash[data_key] = str(data_hash.get(data_key))
                update_sql += "`" + data_key + "` = '" + str(data_hash[data_key]) + "',"
            update_sql = update_sql[:-1]
            if condition:
                update_sql = update_sql + ' ' + condition
            logger.debug(update_sql)
        result = self.query(update_sql)
        return result.get('rows') if result else False


if __name__ == '__main__':
    # from flask_app.utils.mysql_interface import MysqlInterface
    mi = MysqlInterface()
    # 增
    print(mi.insert('test', {"id": 5, "name": 'qjj'}))

    # 删
    # print(mi.delete('wangwangdb', 'test', "where count = '4' and tomember = 'Shmily'"))

    # 改
    # print(mi.update('wangwangdb', 'test', {"count": 4, "tomember": 'zxw'}, "where count = 3 and tomember = '123'"))

    # 查
    print(mi.query("show databases"))
    print(mi.query("select * from test limit 10"))
    print(mi.get_pd("select * from test limit 10"))

    # 获取jdbc链接
    print(mi.get_conn_link())

    # 获取pd对象


    # 获取class信息
    print(mi.get_conn_info())
