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
    print(res_mb, name)


"""
lsof -p PID

ps -aux |sort -k4nr | head -n 40 |tr -s ' '|cut -d ' ' -f 1,4,11

ps -eo pmem,pcpu,rss,vsize,args | sort -k 1 -n -r | less


ps -aux |sort -k4nr | grep task_id= | head -n 40 |tr -s ' '|cut -d ' ' -f 1,4,15


ps -aux |sort -k4nr | grep task_id=app.cc_crash_email_push
"""

