#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: python高阶函数 map的reduce
:Owner: jiajing_qu
:Create time: 2019/11/1 9:40
"""
"""
map对列表中每个元素进行操作后返回列表
reduce对列表中每个元素相加与合并后返回一个值 聚合操作
"""

base_list=['q','j','j','1','2','3']
map_list = map(lambda x: x+"_",base_list)
print(map_list)

reduce_list = reduce(lambda x, y: x+"_"+y,base_list)
print(reduce_list)
reduce_list_join = "_".join(base_list)  # 等价
print(reduce_list_join)

# list中有多个dict的情况,结合使用map和reduce
base_dict_list=[
    {'qjj':'test1'},
    {'qjj':'test2'},
    {'qjj':'test3'}
]
content = reduce(lambda x, y: x+"\n"+y, map(lambda x: x.get('qjj'), base_dict_list))
print(content)