#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 多益 链表删除
:Author: 佳境Shmily
:Create Time: 2020/4/2 15:46
:File: duoyi_01
:Site: shmily-qjj.top

给定一个单向链表和整数n，删除该链表倒数第n个节点，返回链表头节点，这里假定n合法的，时间复杂度要求O(n)
1->2->3->4->5   n=2
"""

class Node(object):
    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next


class LinkedList(object):
    def __init__(self):
        self._head = None
        self._size = 0

    def append(self, value):
        new_node = Node(value)
        if not self._head:
            self._head = new_node
        else:
            current_node = self._head
            while current_node.next:
                current_node = current_node.next
            current_node.next = new_node
        self._size += 1

    def remove(self, n):
        if self._size == 0:
            return
        elif self._size == 1:
            self.__init__()
        elif self._size == n:
            self._head = self._head.next
        else:
            # need_remove_idx = self._size - n    # 要删除节点的前一个节点
            need_remove_pre_idx = self._size - n - 1  # 要删除节点的前一个节点
            current_node = self._head
            current_idx = 0
            while current_node:
                if current_idx == need_remove_pre_idx:
                    current_node.next = current_node.next.next
                    break
                else:
                    current_node = current_node.next
                    current_idx += 1
        self._size -= 1
        return self._head.value




    def __str__(self):
        if self._size == 0:
            return
        result_list = []
        current_node = self._head
        while current_node:
            result_list.append(str(current_node.value))
            current_node = current_node.next
        return '->'.join(result_list)


if __name__ == '__main__':
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.append(4)
    ll.append(5)
    print(ll.remove(2))
    print(ll)
