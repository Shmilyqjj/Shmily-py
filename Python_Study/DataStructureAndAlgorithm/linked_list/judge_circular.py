#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 判断一个链表是否是循环链表   思路：快慢指针
:Author: 佳境Shmily
:Create Time: 2020/4/23 15:10
:File: judge_circular
:Site: shmily-qjj.top
快慢指针解决的问题不光可以判断循环链表，还可以找链表的中间值
:Reference:https://www.jianshu.com/p/21b4b8d7d31b
"""
from Python_Study.DataStructureAndAlgorithm.linked_list.circular_linked_list import CircularLinkedList
from Python_Study.DataStructureAndAlgorithm.linked_list.linked_list import LinkedList

def judge_circular(node):
    """
    双指针法  判断是否为循环链表  一个快指针 一个慢指针 如果最后还能相遇，则是循环链表，否则不是循环链表
    :param node: 链表中一个节点
    :return:
    """
    fast = node  # 一次走两步
    slow = node   # 一次走一步
    while fast and fast.get_next():   # 快慢指针 while条件是 fast指针存在且fast的下一个节点存在（因为fast一次走两步）
        slow = slow.get_next()
        fast = fast.get_next().get_next()
        if slow == fast:
            return True
    return False



if __name__ == '__main__':
    ll = LinkedList()
    ll.add(1)
    ll.add(2)
    ll.add(3)
    ll.add(4)
    ll.show()

    cll = CircularLinkedList()
    cll.add(1)
    cll.add(2)
    cll.add(3)
    cll.add(4)
    cll.show()

    print(judge_circular(ll._head))   # False
    print(judge_circular(cll._head))  # True