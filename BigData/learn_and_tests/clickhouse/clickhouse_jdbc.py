#!/usr/bin/env python
# encoding: utf-8
"""
:Description: clickhouse jdbc conn
:Author: 佳境Shmily
:Create Time: 2022/2/23 9:52
:File: clickhouse_jdbc
:Site: shmily-qjj.top
: pip install clickhouse-driver
"""


from clickhouse_driver import Client
client = Client(host='192.168.2.101', port='9030', user='default', password='')
ans = client.execute('desc default.table;')
cols = list(map(lambda x: x[0], ans))



p1_cols = list(map(lambda x: x[0], Client(host='192.168.2.101', port='9009', user='default', password='').execute('desc default.table1;')))
p2_cols = list(map(lambda x: x[0], Client(host='192.168.2.102', port='9009', user='default', password='').execute('desc db1.table2;')))
p3_cols = list(map(lambda x: x[0], Client(host='192.168.2.103', port='9009', user='default', password='').execute('desc db1.table2;')))
p4_cols = list(map(lambda x: x[0], Client(host='192.168.2.104', port='9009', user='default', password='').execute('desc db1.table2;')))


l = list(set(p1_cols).intersection(set(p2_cols)).intersection(set(p3_cols)).intersection(set(p4_cols)))