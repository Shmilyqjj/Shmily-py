#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 输入一个字符串s，返回含有两个s作为子串的最短字符串  注意两个s可能会有重叠部分(aba返回ababa)
:Author: 佳境Shmily
:Create Time: 2020/4/2 21:25
:File: solution01
:Site: shmily-qjj.top
思路 只要找出最长首尾重叠部分即可
"""

def solution(s):
    if not s:
        return
    length = len(s)
    if length == 1:
        return s * 2
    repeat_length = 0
    for i in range(1, length):
        if s[:i] == s[(length - i):]:  # i = 1 首尾最长重叠部分为a 第二部分的a前面是ab ，后面是ba  所以结果ababa
            repeat_length = i
    return s + s[repeat_length:]


if __name__ == '__main__':
    s = input()
    print(solution(s))