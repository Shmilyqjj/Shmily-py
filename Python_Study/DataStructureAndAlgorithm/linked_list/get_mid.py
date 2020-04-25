#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 获取链表的中间元素    适用单链表
:Author: 佳境Shmily
:Create Time: 2020/4/25 9:54
:File: get_mid
:Site: shmily-qjj.top
"""
from Python_Study.DataStructureAndAlgorithm.linked_list.linked_list import LinkedList

def get_mid(node):
    """
    获取中间元素
    :param node: 链表的head
    :return: 中间值
    """
    fast = node
    slow = node
    while fast and fast.get_next():
        slow = slow.get_next()
        fast = fast.get_next().get_next()
    return slow.get_value()


if __name__ == '__main__':
    ll = LinkedList()
    ll.add(1)
    ll.add(2)
    ll.add(3)
    ll.add(4)
    ll.add(5)
    ll.add(6)
    ll.add(7)

    print(get_mid(ll._head))
