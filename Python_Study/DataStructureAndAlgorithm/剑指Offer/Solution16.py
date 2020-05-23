#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 16
:Author: 佳境Shmily
:Create Time: 2020/4/28 11:59
:File: Solution16
:Site: shmily-qjj.top
输入两个单调递增的链表，输出两个链表合成后的链表，当然我们需要合成后的链表满足单调不减规则。

考察递归和链表
"""
class ListNode:
    def __init__(self, x, n=None):
        self.val = x
        self.next = n


class Solution:
    def Merge(self, pHead1, pHead2):
        # 递归方法
        # write code here
        if not pHead1:
            return pHead2
        if not pHead2:
            return pHead1
        if pHead1.val <= pHead2.val:
            pHead1.next = self.Merge(pHead1.next, pHead2)
            return pHead1
        else:
            pHead2.next = self.Merge(pHead1, pHead2.next)
            return pHead2


if __name__ == '__main__':
    s = Solution()
    l1 = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    l2 = ListNode(6, ListNode(7, ListNode(8, ListNode(9, ListNode(10)))))