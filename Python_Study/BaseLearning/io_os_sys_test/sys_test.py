#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description:  sys模块使用
:Owner: jiajing_qu
:Create time: 2020/1/9 0:03
"""

import sys

python_search_module_list = sys.path   # python的搜索模块的路径集，是一个list
print(python_search_module_list)

print("#########################################################################")

print(sys.argv[0],sys.argv[1],sys.argv[2])  # 传参  argv[0]与linux的shell脚本一样，都是文件本身路径  argv[1]开始才是人为传的参数  超过就会list out of range可见sys.argv本身就是list  （在pycharm添加两个参数）

print("#########################################################################")

print(sys.getdefaultencoding())
reload(sys)
sys.setdefaultencoding('utf-8')

print("#########################################################################")


sys.exit(-1)
