#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 
:Owner: jiajing_qu
:Create time: 2019/10/10 12:03
"""

import os
import traceback
from hdfs import *
import getpass
from snakebite.client import HAClient
from snakebite.namenode import Namenode


def get_hdfs_client():
    """
    获得 HDFS Client
    :return: HDFS Client
    """
    client = InsecureClient("http://hadoop101:50070;http://hadoop102:50070", user=getpass.getuser())
    return client


def get_snakebite_hdfs_client():
    """
    获得 snakebite库的HDFS Client
    :return: snakebite HDFS Client
    """
    n1 = Namenode("hadoop101", 9000)
    n2 = Namenode("hadoop102", 9000)
    client = HAClient([n1, n2], effective_user="hdfs", sock_request_timeout=10000000000)
    return client


def get_hdfs_files(client,path):
    """
    遍历HDFS文件 得到文件全路径的大小
    :param client: HDFS Client
    :param path: 指定HDFS文件夹
    :return: 一个dict {绝对路径:文件大小}
    """
    results_dict = {}
    try:
        for root, dirs, files in client.walk(path, status=False):
            for file in files:
                full_path = os.path.join(root, file)
                length = client.status(full_path)['length']
                results_dict[full_path] = length
    except:
        traceback.print_exc()
    return results_dict


def delete_small_parquet(client,results_dict):
    """
    删除小于等于4字节的文件
    :param client:
    :param results_dict:
    :return:
    """
    for f, size in results_dict.items():
        if size <= 4:
            if client.delete(f):
                print("成功删除小文件 %s" % f)
            else:
                print("删除小文件 %s 失败" % f)


def main():
    """
    主函数入口
    :return:
    """
    HDFS_CLIENT = get_hdfs_client()  # hdfs客户端获取
    path = "/data_test/tong/test_small_parqute"
    results_dict = get_hdfs_files(HDFS_CLIENT, path)
    delete_small_parquet(HDFS_CLIENT, results_dict)


if __name__ == '__main__':
    main()


