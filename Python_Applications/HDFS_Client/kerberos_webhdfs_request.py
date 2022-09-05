#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: python访问kerberos认证的webhdfs
:Owner: shmily
:Create time: 2022/9/5 14:03
:Dependencies: pip3 install setuptools_rust requests-kerberos krbcontext
"""
import requests
from requests_kerberos import HTTPKerberosAuth

active_nn_addr = 'http://nn1:50070'
response = requests.get(f'{active_nn_addr}/webhdfs/v1/?op=LISTSTATUS', auth=HTTPKerberosAuth())
if response.status_code == 200:
    print(response.json())
elif response.status_code == 403:
    print("请使用活动的namenode地址")
    print(response.text)
else:
    print("其他错误")

