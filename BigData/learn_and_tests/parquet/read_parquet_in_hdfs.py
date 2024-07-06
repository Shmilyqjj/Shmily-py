#!/usr/bin/env python
# encoding: utf-8
"""
:Description:
:Author: 佳境Shmily
:Create Time: 2021/12/25 10:11
:File: read_parquet
:Site: shmily-qjj.top
"""
from fastparquet import ParquetFile
from hdfs3 import HDFileSystem


def read_parquet_on_hdfs():
    """
    Read Parquet File on HDFS
    :return:
    """
    hdfs = HDFileSystem(host="192.168.1.101", port=8020)
    sc = hdfs.open
    pf = ParquetFile("/user/hive/warehouse/test.db/test.parquet", open_with=sc)
    print(pf.to_pandas())


def read_parquet_on_ha_hdfs():
    """
    Read parquet file on HA mode hdfs
    :return:
    """

    ns = "nameservice1"
    conf = {
        "dfs.nameservices": "nameservice1",
        "dfs.ha.namenodes.nameservice1": "namenode113,namenode188",
        "dfs.namenode.rpc-address.nameservice1.namenode113": "hostname_of_server1:8020",
        "dfs.namenode.rpc-address.nameservice1.namenode188": "hostname_of_server2:8020",
        "dfs.namenode.http-address.nameservice1.namenode113": "hostname_of_server1:50070",
        "dfs.namenode.http-address.nameservice1.namenode188": "hostname_of_server2:50070",
        "hadoop.security.authentication": "kerberos"
    }
    hdfs = HDFileSystem(host=ns, pars=conf)
    sc = hdfs.open
    pf = ParquetFile("/user/hive/warehouse/test.db/test.parquet", open_with=sc)
    print(pf.to_pandas())


def read_parquet_on_local():
    """
    Read local parquet file
    :return:
    """
    pf = ParquetFile("E:\\test.parquet")
    print(pf.to_pandas())


if __name__ == '__main__':
    # read_parquet_on_hdfs()
    read_parquet_on_local()