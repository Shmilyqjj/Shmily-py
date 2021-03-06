#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
Description:
Author:jiajing_qu
Date: 2019/9/15 19:44

穿越障碍物
时间限制：C/C++语言 1000MS；其他语言 3000MS
内存限制：C/C++语言 65536KB；其他语言 589824KB
题目描述：
你现在在(0,0)，需要到(x,y)去，路上有n个障碍物。给出每个障碍物的坐标，你只能平行于坐标轴走整数步，问你最少需要多少步才能走到目的地。

输入
第一行三个数x,y,n

接下来n行，每行描述一个障碍物的坐标x_i,y_i

-500≤x,y,x_i,y_i≤500

n≤10000

保证有解

输出
输出一个数，代表最少的步数。


样例输入
2 0 3
1 0
1 1
1 -1
样例输出
6

"""
