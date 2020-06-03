#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
Description:
Author:曲佳境
Date: 2019/9/10 20:03
"""

dic = {
    2:['1'],
    3:['7'],
    4:['4'],
    5:['2','3','5'],
    6:['6','9'],
    7:['8']
}

xjb ={
    1:1/2,
    2:2/5,
    3:3/5,
    4:4/4,
    5:5/5,
    6:6/6,
    7:7/3,
    8:8/7,
    9:9/6
}

# dic0 = {
#     2:1,
#     3:7,
#     4:4,
#     5:5,
#     6:9,
#     7:8
# }

n,m = map(int,input().split())
can = []
l = []
for i in range(m):
    can.append(input())
for k,v in dic.items():
    for w in v:
        for c in can:
            if c in w:
                l.append(k)
 # l = 3 4 5 7 根 每个数
sorted(l)
print(l)
for i in range(len(l)):
    for j in range(len(l)-i-1):
        pass
    #....





