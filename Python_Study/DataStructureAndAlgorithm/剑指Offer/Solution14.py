#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 14
:Author: 佳境Shmily
:Create Time: 2020/4/28 11:59
:File: Solution14
:Site: shmily-qjj.top
输入一个链表，输出该链表中倒数第k个结点。
"""


class ListNode:
    def __init__(self, x, n=None):
        self.val = x
        self.next = n


class Solution:
    # def FindKthToTail(self, head, k):
    #     # write code here
    #     # 使用栈  不考虑空间复杂度
    #     l = []
    #     current_node = head
    #     while current_node:
    #         l.append(current_node)   # 因为要返回节点 而不是 节点的val
    #         current_node = current_node.next
    #     if k > len(l):
    #         return
    #     if k == 0:
    #         return
    #     return l[len(l) - k]


    def FindKthToTail(self, head, k):
        # write code here
        """
        双指针  思路：fast先走 如果fast不能走到k 返回null   能走到k，走到k时，slow和fast同步走，fast走到头的时候 slow即为所求。
        :param head: 头结点
        :param k: 倒数第k个元素
        :return:
        """
        if not head or k <= 0:
            return
        fast = head
        slow = head
        while k > 1:  # fast先走到索引k-1处  即链表前k个元素处   如果走不到则越界返回None
            if fast.next:
                fast = fast.next
                k -= 1
            else:
                return
        # 如果能走到k-1处  slow与fast开始同步走  fast走到终点时，slow即为所求
        while fast.next:
            fast = fast.next
            slow = slow.next
        return slow


if __name__ == '__main__':
    h = ListNode(1, ListNode(2, ListNode(3,ListNode(4,ListNode(5)))))
    s = Solution()
    print(s.FindKthToTail(h, 5).val)

