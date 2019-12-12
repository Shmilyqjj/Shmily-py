#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: MongoDB 工具类
:Owner: jiajing_qu
:Create time: 2019/11/1 14:04
"""
import os
print("******************检测pymongo环境*********************")
print(os.popen('pip show pymongo').read())
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
print("*****************************************************")
import pymongo
import traceback
import time


class MongoOperation(object):
    """
      mongo 对一个已有库的所有操作
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(MongoOperation, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, host, port, user, password, db, table=None):
        """
        初始化类
        :param host:  mongo host
        :param port:  mongo端口  int类型
        :param user:  连接的用户
        :param password:  密码
        :param db:  db
        :param table:  tb
        """
        try:
            # 需要对已只的表操作,新增,修改,查询时，需要传入table
            self.MongoClient = pymongo.MongoClient(host, port)
            # what's this?
            # MongoClient.slave_okay = True
            self.MongoDb = self.MongoClient[db]
            # 需要认证
            self.MongoDb.authenticate(user, password)
        except ConnectionFailure:
            raise Exception("ConnectionFailure")
        except OperationFailure:
            raise Exception("OperationFailure")
        except Exception:
            e = traceback.format_exc()
            # print str(e)
            # traceback.print_exc()
            raise Exception("other failure")
        if table is not None:
            self.table = table

    def getTable(self):
        """
        获取的table 返回mongo的collection
        :return:
        """
        if self.table in self.MongoDb.list_collection_names():
            feedCol = self.MongoDb[self.table]
            return feedCol
        raise Exception("not exist table:%s" % self.table)

    def createTable(self, table, **kwargs):
        """
        新建表
        :return:
        """
        self.MongoDb.create_collection(table, **kwargs)

    def showTables(self):
        return self.MongoDb.list_collection_names()

    def dropTable(self, table):
        """
            删除数据表或者集合
        :param table:
        :return:
        """
        self.MongoDb.drop_collection(table)

    def insert(self, dict_data):
        """
        插入数据
        :param dict_data:
        :return:
        """
        feedCol = self.getTable()
        if dict_data:
            dict_data.update({"create_time": time.time()})
            return feedCol.insert(dict_data)
        else:
            pass

    def insert_many(self, list_dict_data):
        """
        批量添加
        :param list_dict_data:
        :return:
        """
        if list_dict_data:
            list_dict_data_new = []
            for each in list_dict_data:
                each.update({"create_time": time.time()})
                list_dict_data_new.append(each)
            feedCol = self.getTable()
            return feedCol.insert_many(list_dict_data_new)
        else:
            pass

    def find(self, condition_dict=None, limit=10):
        """
        查数据,根据条件查看数据
        :param condition_dict:
        :return:
        """
        feedCol = self.getTable()
        return list(feedCol.find(condition_dict).limit(limit))

    def delete(self, condition):
        """
        删除文档数据
        :param condition:
        :return:
        """
        feedCol = self.getTable()
        feedCol.delete_many(condition)

    def update(self, condition):
        """
        修改文档
        :param condition:
        :return:
        """
        feedCol = self.getTable()
        feedCol.update_many(condition)

    def get_mongo_jdbc_count(self):
        """
        mongo JDBC获取到的数据量统计
        :return:
        """
        st = time.time()
        collection = self.getTable()
        mongo_jdbc_count = collection.count()
        et = time.time()
        print("检测到Mongo collection数据量: %s  耗时: %s" % (mongo_jdbc_count, et - st))
        return mongo_jdbc_count