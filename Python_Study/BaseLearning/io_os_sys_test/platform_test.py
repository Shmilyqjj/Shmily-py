#!/usr/bin/env python
# encoding: utf-8
"""
:Author: jiajing_qu
:Create Time: 2020/1/21 15:30
:@File: platform_test.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""

import platform

print(platform.machine())  # 返回平台架构
print(platform.node())  # 返回主机名

print(platform.platform())  # 返回系统OS名
print(platform.platform(aliased=True,terse=True))  # 返回系统OS名
print (platform.system())  # 返回系统名称

print(platform.processor())  # 返回处理器名

print(platform.architecture())  # 位数32 64

print('******************************')

print(platform.uname())  # 包含上面的总信息

def get_python_info():
    platform.python_build()
    platform.python_compiler()
    platform.python_branch()
    platform.python_implementation()
    platform.python_revision()
    platform.python_version()
    platform.python_version_tuple()
