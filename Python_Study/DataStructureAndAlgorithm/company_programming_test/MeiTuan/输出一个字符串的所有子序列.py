#!/usr/bin/env python
# encoding: utf-8
"""
:Description:输出一个str的所有子序列
:Author: 佳境Shmily
:Create Time: 2020/4/19 22:12
:File: 输出一个str的所有子序列 aaa的子序列 a(1),a(2),a(3),aa(12),aa(23),aa(13),aaa(123)
:Site: shmily-qjj.top

以arr=[1,2,3]为例，用01二进制串决定子序列中的每个数字是否输出。0表示该位置上的数字不存在，1表示该位置上的数字存在
子序列如果是空集[]，就用000表示，因为[1,2,3]中没有元素存在；子序列中如果只有元素1存在，则按照原来数组中的位置来说表示位100；同理只有元素2存在，则表示为010；元素2存在，表示为001；如果元素1和2同时存在表示为110；三个数字都存在表示为111
[]=000;[1]=100;[2]=010;[3]=001;[1,2]=110;……[1,2,3]=111

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