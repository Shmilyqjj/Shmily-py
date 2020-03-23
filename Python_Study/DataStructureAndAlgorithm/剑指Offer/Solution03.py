#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 03
:Author: 佳境Shmily
:Create Time: 2020/3/23 9:40
:File: Solution03
:Site: shmily-qjj.top


输入一个链表，按链表从尾到头的顺序返回一个ArrayList。
"""

# -*- coding:utf-8 -*-
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    # 返回从尾部到头部的列表值序列，例如[1,2,3]
    def printListFromTailToHead(self, listNode):
        current_node = listNode
        arr = []
        while current_node:
            arr.append(current_node.val)
            current_node = current_node.next
        arr.reverse()
        return arr


if __name__ == '__main__':
    s = Solution()
    # s.printListFromTailToHead({67,0,24,58})
    arr = [1,2,3,4,5]
    arr.reverse()
    print(arr)