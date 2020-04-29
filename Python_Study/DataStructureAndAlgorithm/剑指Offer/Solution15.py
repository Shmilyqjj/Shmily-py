#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 15
:Author: 佳境Shmily
:Create Time: 2020/4/28 11:59
:File: Solution15
:Site: shmily-qjj.top
输入一个链表，反转链表后，输出新链表的表头。

觉得一个巧妙的思路很重要   这个题 递归和非递归 两种方法 都比较经典

理解起来有点难度
"""
class ListNode:
    def __init__(self, x, n=None):
        self.val = x
        self.next = n


class Solution:
    # 返回ListNode
    def ReverseList(self, pHead):
        # write code here
        # 解法1 非递归   很巧妙
        if not pHead or not pHead.next:  # 如果空链表或链表只有一个元素  返回原链表
            return pHead
        # 链表反转
        pre = None
        current = pHead
        while current:  # 1->2->3->4->5 把1的next置为None，2的next置为1 以此类推 得到反转链表
            next = current.next  # 当前节点的下一个节点保存为next
            current.next = pre  # 当前节点的next置为pre
            pre = current  # pre变当前节点  pre current同时移动  重复这个步骤
            current = next  # 当前节点变next
        return pre


    # def ReverseList(self, pHead):
    #     # write code here
    #     # 解法2 递归
    #     if not pHead or not pHead.next:  # 如果链表为空或者只有一个元素
    #         return pHead
    #     result = self.ReverseList(pHead.next)  # 先反转后面的链表
    #     # 再将当前节点设置为后面节点的后续节点
    #     pHead.next.next = pHead
    #     pHead.next = None
    #     return result





if __name__ == '__main__':
    s = Solution()
    h = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    print(s.ReverseList(h).val)

