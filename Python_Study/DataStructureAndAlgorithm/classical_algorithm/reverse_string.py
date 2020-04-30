#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 翻转字符串
:Author: 佳境Shmily
:Create Time: 2020/4/30 13:15
:File: reverse_string
:Site: shmily-qjj.top

双指针 交换 直到 两个指针相遇 退出
"""

def reverse_string(s):
    if not s or len(s) == 1:
        return s
    head = 0  # 头结点 索引
    tail = len(s) - 1   # 尾结点 索引
    s = list(s)  # 转换为list 支持交换
    while head != tail:
        s[head], s[tail] = s[tail], s[head]
        head += 1
        tail -= 1
    return "".join(s)


if __name__ == '__main__':
    print(reverse_string("mhtirogla"))