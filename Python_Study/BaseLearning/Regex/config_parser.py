#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: ConfigParser是一个好用的工具可以方便又规范地获取配置文件中的信息 ConfigParser在python中用来读取ini类型的配置文件的，提供很多方便的API使用。
:Owner: jiajing_qu
:Create time: 2019/11/15 15:28
"""

"""
ini文件结构需要注意一下几点：
键值对可用=或者:进行分隔
section的名字是区分大小写的,而key的名字是不区分大小写的
键值对中头部和尾部的空白符会被去掉
值可以为多行
配置文件可以包含注释，注释以#或者;为前缀
"""



try:
    import ConfigParser    # python2中的名字是ConfigParser
except:
    import configparser as ConfigParser    # python3中的名字是configparser

# 获取mysql配置文件my.cnf的[mysqld]下的所有参数配置
file_abs_path = 'my.cnf'
parser = ConfigParser.SafeConfigParser()
if parser.read(file_abs_path):   # 读配置文件
    tuples = parser.items('mysqld')  # 获取mysqld下所有参数
    print(tuples)
# 我们想得到symbolic-links这个参数的值:
    symbolic_links = reduce(lambda x, y: dict(x, **y), map(lambda x: {x[0]: x[1]}, parser.items('mysqld'))).get('symbolic-links')
    print(symbolic_links)

print(parser.sections())   # 获取[]里的条目

# 其他参考 https://blog.csdn.net/weixin_42174361/article/details/82873878

