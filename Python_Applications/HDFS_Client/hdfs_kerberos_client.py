#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: python访问kerberos hdfs
:Owner: shmily
:Create time: 2022/9/5 12:03
:Dependencies: pip3 install setuptools_rust requests-kerberos krbcontext hdfs
"""
from hdfs.ext.kerberos import KerberosClient
from krbcontext import krbcontext

keytab_file = '/etc/ecm/hadoop-conf/hdfs.keytab'
principal = 'hdfs/emr-header-host@EXAMPLE.COM'
namenode_urls = 'http://nn1:50070;http://nn2:50070'

with krbcontext(using_keytab=True, keytab_file=keytab_file, principal=principal, ccache_file='/tmp/cache_keytab_zds'):
    client = KerberosClient(url=namenode_urls)
    client.status('/tmp')
    client.content('/tmp')
