#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: time/datetime总结
:Owner: jiajing_qu
:Create time: 2019/9/23 17:09
"""
import time
import datetime

# 时间戳 float
timestamp = time.time()
print(timestamp)

# 时间元组 struct_time
localtime = time.localtime(time.time())
print(localtime)

# Thu Apr 7 10:05:21 2019
localtime = time.asctime( time.localtime(time.time()) )
print (localtime)

#格式化日期
format_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(format_time)
format_time = time.strftime("%Y-%m-%d %H:%M:%S")
print(format_time)

#字符串转时间戳
a = "Sat Mar 28 22:24:24 2019"
print time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y"))

# datetime获取当前日期和时间
now = datetime.datetime.now()
print(now)

#用指定日期时间创建datetime
dt = datetime.datetime(2019, 9, 23, 17, 20)
print(type(dt))
print(dt)

#datetime获取日月年等
dt = datetime.datetime(2019, 9, 23, 17, 20)
dt.day
dt.year
dt.month
dt.minute

#datetime转Str
now = datetime.datetime.now()
print(now.strftime('%a, %b %d %H:%M'))

#timestamp转datetime
t = 1429517200.0
print(datetime.datetime.fromtimestamp(t))

#字符串转datetime
str_to_dt = datetime.datetime.strptime('2019-10-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print(str_to_dt)

#格式化时间,多加一天,减一天 加小时,减分钟
n = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
print ('+1 day',(datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))
print ('-1 day',(datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S"))
# days改为hours minutes

# datetime的差值为datedelta
d1 = datetime.datetime.now()  # datetime
time.sleep(3)
d2 = datetime.datetime.now()  # datetime
d3 = d2 - d1   # timedelta格式
print(d3.seconds)  # 秒
print(d3.total_seconds()) # 秒+微秒




