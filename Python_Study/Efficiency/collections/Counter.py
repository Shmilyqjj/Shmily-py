#!/usr/bin/env python
# encoding: utf-8
"""
:Description:使用collections.Counter加速计数
:Author: 佳境Shmily
:Create Time: 2020/7/26 23:52
:File: demo
:Site: shmily-qjj.top
"""
import time
data = [x**2 % 1989 for x in range(2000000)]

st = time.time()
values_count = {}
for i in data:
    i_cnt = values_count.get(i, 0)
    values_count[i] = i_cnt + 1
print(values_count.get(4, 0))
print("time: %s" % (time.time() - st))


st = time.time()
from collections import Counter
values_count = Counter(data)
print(values_count.get(4, 0))
print("time: %s" % (time.time() - st))