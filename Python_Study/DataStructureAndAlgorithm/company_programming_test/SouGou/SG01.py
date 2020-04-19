#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
Description:搜狗笔试2019秋招
Author:曲佳境
Date: 2019/9/8 18:04
python2环境
"""
import re
n,m = map(int,input().split(" "))
rules = []
ips = []
for i in range(n):
    rules.append(input())
for j in range(m):
    ips.append(input())
for i in range(len(rules)):
    for j in range(len(ips)):
        if j<=len(ips):
            if re.match("[.*%s.*]" % rules[i],ips[j]):
                print(1,end=" ")
                ips.remove(ips[j])
            else:
                print(0,end=" ")
                ips.remove(ips[j])
        else: break


