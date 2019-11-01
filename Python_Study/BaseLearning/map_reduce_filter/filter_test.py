#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 高阶函数filter 测试
:Owner: jiajing_qu
:Create time: 2019/11/1 9:50
"""
"""
filter 用于按一定条件筛选列表中的元素 过滤功能
"""

base_list = [1,2,3,4,5,6,7,8,9,10]
filtered_list = filter(lambda x: x>5,base_list)
print(filtered_list)