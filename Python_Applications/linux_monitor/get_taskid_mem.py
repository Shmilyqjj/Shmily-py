#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: linux系统获得进程的task_id和mem
:Owner: jiajing_qu
:Create time: 2019/10/21 12:13
"""
import os
import re
res = os.popen("ps -aux |sort -k6nr").readlines()
for i in range(len(res)-1):
    res_after = re.sub(' +', ' ', res[i])
    l = res_after.split(" ")
    res_mb = int(l[5]) / 1024
    name = l[len(l)-1].rstrip("\n")
    if name.find("task_id=") >= 0:
        print(res_mb,name)

