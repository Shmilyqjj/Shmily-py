#!/usr/bin/env python
# encoding: utf-8
"""
:Description:
:Author: 佳境Shmily
:Create Time: 2021/12/25 10:10
:File: read_parquet
:Site: shmily-qjj.top
"""


from hdfs3 import HDFileSystem
from fastparquet import ParquetFile


def read_local_parquet(file_name):
    """
    Read Local ParquetFile
    :param file_name1:
    :return:
    """
    pf = ParquetFile(file_name)
    print(pf.columns)
    print(len(pf.columns))
    print(pf.to_pandas())


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


if __name__ == '__main__':
    file_name: str = "F:\\Downloads\\6dc150c9-60d2-419f-9d86-008c7433b155-r-0-6-SG-50-50"
    read_local_parquet(file_name)