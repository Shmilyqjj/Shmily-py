#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 使用collections.ChainMap加速字典合并
:Author: 佳境Shmily
:Create Time: 2020/7/26 23:58
:File: ChainMap
:Site: shmily-qjj.top
"""

# 低速
dict_a = {i: i + 1 for i in range(1, 1000000, 2)}
dict_b = {i: i * 2 + 1 for i in range(1, 1000000, 3)}
dict_c = {i: i * 3 + 1 for i in range(1, 1000000, 5)}
dict_d = {i: i * 4 + 1 for i in range(1, 1000000, 7)}
result = dict_a.copy()
result.update(dict_b)
result.update(dict_c)
result.update(dict_d)
print(result.get(9999))


# 高速
from collections import ChainMap
chain = ChainMap(dict_a, dict_b, dict_c, dict_d)
print(chain.get(9999))
