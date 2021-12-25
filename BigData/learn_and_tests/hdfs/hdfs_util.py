#!/usr/bin/env python
# encoding: utf-8
"""
:Description:
:Author: 佳境Shmily
:Create Time: 2021/12/25 10:24
:File: hdfs_util
:Site: shmily-qjj.top
"""


import pyhdfs
from hdfs3 import HDFileSystem


ns = "nameservice1"
conf = {
    "dfs.nameservices": "nameservice1",
    "dfs.ha.namenodes.nameservice1": "namenode113,namenode188",
    "dfs.namenode.rpc-address.nameservice1.namenode165": "nn1_ip:8020",
    "dfs.namenode.rpc-address.nameservice1.namenode129": "nn2_ip:8020",
    "dfs.namenode.http-address.nameservice1.namenode165": "nn1_ip:9870",
    "dfs.namenode.http-address.nameservice1.namenode129": "nn2_ip:9870",
    "hadoop.security.authentication": "kerberos"
}
hdfs = HDFileSystem(host=ns, pars=conf)
sc = hdfs.open