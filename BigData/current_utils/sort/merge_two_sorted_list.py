#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 归并两个有序list
:Author: 佳境Shmily
:Create Time: 2020/4/21 13:13
:File: merge_two_sorted_list
:Site: shmily-qjj.top
假设两个lsit a b都是有序且同时为正序或倒序
这个问题属于归并排序中的归并部分 一个子问题
字节2020春招
"""
a = [1,2,5,7]
b = [2,3,4,6]

def merge(a, b):
    result = []
    i, j = 0, 0
    while i < len(a) and j < len(b):  # 遍历a和b
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result += a[i:]
    result += b[j:]
    return result

print(merge(a, b))
