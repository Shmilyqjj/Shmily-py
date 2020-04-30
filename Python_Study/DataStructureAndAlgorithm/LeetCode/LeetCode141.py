#!/usr/bin/env python
# encoding: utf-8
"""
:Description: LeetCode 141. 环形链表  判断链表中是否有环
:Author: 佳境Shmily
:Create Time: 2020/4/30 23:38
:File: LeetCode141
:Site: shmily-qjj.top
思路：快慢指针
原题：https://leetcode-cn.com/problems/linked-list-cycle/
"""

# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        # 双指针法 一快一慢
        fast = head
        slow = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if slow == fast:
                return True
        return False