#!/usr/bin/env python
# encoding: utf-8
"""
:Description: set集合操作
:Author: 佳境Shmily
:Create Time: 2020/6/25 23:01
:Site: shmily-qjj.top
"""
i = set([1, 2, 3, 4, 5, 6, 6, 7, 7])
j = set([1, 2, 2, 2, 2, 2, 3, 3, 8])

print(i, j)

print(i & j)
print(i | j)
print(i ^ j)
print(i - j)

