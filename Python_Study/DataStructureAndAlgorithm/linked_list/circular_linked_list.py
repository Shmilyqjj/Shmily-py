#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 循环链表
:Author: 佳境Shmily
:Create Time: 2020/3/17 21:37
:File: circular_linked_list
:Site: shmily-qjj.top
单链表判断循环结束为：node->next==NULL;而循环链表判断循环结束为：（node->next）等于头结点
"""

class Node(object):
    def __init__(self, value):
        self._value = value
        self._next = None

    def get_value(self):
        return self._value

    def get_next(self):
        return self._next

    def set_value(self, value):
        self._value = value

    def set_next(self, node_obj):
        self._next = node_obj


class CircularLinkedList(object):
    def __init__(self):
        self._head = None
        self._tail = None
        self._length = 0

    def is_empty(self):
        return self._length == 0

    def get_length(self):
        return self._length

    def add(self, value):
        new_node = Node(value)
        if self.is_empty():
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.set_next(new_node)
            new_node.set_next(self._head)
            self._head = new_node
        self._length += 1

    def append(self, value):
        if self.is_empty():
            self.add(value)
        else:
            new_node = Node(value)
            new_node.set_next(self._head)
            self._tail.set_next(new_node)
            self._tail = new_node
        self._length += 1

    def replace(self, index, value):
        if index >= self._length:
            raise Exception("CircularLinkedList index out of range.")
        current_node = self._head
        current_index = 0
        while current_node:
            if current_index == index:
                current_node.set_value(value)
                break
            else:
                current_node = current_node.get_next()
                current_index += 1

    def search(self, value):
        current_node = self._head
        while current_node:
            if current_node.get_value() == value:
                return True
            else:
                current_node = current_node.get_next()
            if current_node.get_next() == self._head:
                break
        return False

    def index(self, value):
        # index索引元素在链表中的位置
        result_list = []
        current_node = self._head
        current_index = 0
        while current_node:
            if current_node.get_value() == value:
                result_list.append(current_index)
            current_node = current_node.get_next()
            current_index += 1
            if current_index == self._length:
                break
        if result_list:
            return result_list
        else:
            return -1

    def get(self, index):
        if index >= self._length:
            raise Exception("CircularLinkedList index out of range.")
        current_index = 0
        current_node = self._head
        while current_node:
            if current_index == index:
                return current_node.get_value()
            else:
                current_node = current_node.get_next()
            current_index += 1

    def remove_by_index(self, index):
        current_node = self._head
        if index >= self._length:
            raise Exception("CircularLinkedList index out of range.")
        elif index == 0:
            # new_head = current_node.get_next()
            # self._head = new_head
            # self._tail.set_next(self._head)
            raise Exception("The Head Node is not allowed to remove.")
        else:
            current_index = 1
            pre_node = self._head
            current_node = pre_node.get_next()
            while current_node:
                if current_index == index:
                    pre_node.set_next(current_node.get_next())
                    break
                else:
                    pre_node = current_node
                    current_node = current_node.get_next()
                current_index += 1
        self._length -= 1

    def remove(self, value, first=True):
        pre_node = self._head
        current_node = pre_node.get_next()
        current_index = 1
        if pre_node.get_value() == value:
            raise Exception("The Head Node is not allowed to remove.")
        if first:
            while current_node:
                if current_node.get_value() == value:
                    pre_node.set_next(current_node.get_next())
                    self._length -= 1
                    break
                else:
                    pre_node = current_node
                    current_node = current_node.get_next()
                current_index += 1
                if current_index == self._length:
                    raise Exception("Value '%s' Not In This CircularLinkedList." % value)
        else:
            pass

    def insert(self, index, value):
        current_index = 1  # current_index下标
        if index == 0:
            self.add(value)
        else:
            pre_node = self._head
            current_node = pre_node.get_next()
            while current_node:
                if index == current_index:
                    new_node = Node(value)
                    new_node.set_next(current_node)
                    pre_node.set_next(new_node)
                    break
                else:
                    pre_node = current_node
                    current_node = current_node.get_next()
                current_index += 1
                if current_index == self._length:
                    break
            self._length += 1

    def clear(self):
        self.__init__()

    def traversal(self, reverse=False):
        """
        遍历 链表
        :param reverse: 默认正向  True为反向结果
        :return: list
        """
        result = []
        current_node = self._head
        if self._length == 0:
            return result
        while True:
            result.append(current_node.get_value())
            if current_node.get_next() != self._head:
                current_node = current_node.get_next()
            else:
                break
        if reverse:
            result = [result[i] for i in range(self._length - 1, -1, -1)]
        return result

    def reverse(self):
        """
        反转单链表
        :return:
        """
        tmp_list = self.traversal()
        self.clear()
        for i in tmp_list:
            self.add(i)

    def show(self):
        if self.is_empty():
            print("Empty CircularLinkedList.")
        else:
            result_list = []
            current_node = self._head
            while current_node:
                result_list.append(current_node.get_value())
                current_node = current_node.get_next()
                if current_node == self._head:
                    break
            result_list = [str(x) for x in result_list]
            print('->'.join(result_list) + "->head")




if __name__ == '__main__':
    cll = CircularLinkedList()
    cll.add(1)
    cll.add(2)
    cll.add(3)
    cll.append(4)
    cll.append(5)
    cll.append(5)
    cll.append(7)
    print(cll.get_length())
    cll.show()
    cll.replace(0, 6)
    cll.replace(1, 7)
    cll.show()
    print(cll.search(7))
    print(cll.search(6))

    print("**************************")
    print(cll.traversal())
    cll.show()
    print(cll.get(2))
    print(cll.get(6))
    # cll.reverse()
    # cll.show()
    print(cll.index(7))

    print("************************")
    cll.show()
    cll.insert(1,8)
    cll.insert(7,9)
    cll.append(10)
    cll.show()
    print(cll.get_length())
    cll.remove_by_index(9)
    cll.show()

    cll.remove(7)
    cll.remove(7)
    cll.remove(7)
    cll.show()



