#!/usr/bin/env python
# encoding: utf-8
"""
:Description:输出一个str的所有子序列
:Author: 佳境Shmily
:Create Time: 2020/4/19 22:12
:File: 输出一个str的所有子序列 aaa的子序列 a(1),a(2),a(3),aa(12),aa(23),aa(13),aaa(123)
:Site: shmily-qjj.top
"""

def sub(arr):
    result = []    # 保存结果
    size = len(arr)
    end = 1 << size    # end=2**size
    for index in range(end):
        array = []    # remember to clear the list before each loop
        for j in range(size):
            if (index >> j) % 2:
                array.append(arr[j])
        # print(array)
        result.append(array)
    result = ["".join(x) for x in result if x]
    return result

if __name__ == '__main__':
    print(sub("aaa"))