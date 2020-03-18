#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 双向链表
:Author: 佳境Shmily
:Create Time: 2020/3/17 21:37
:File: doubly_linked_list
:Site: shmily-qjj.top
学完了单向链表 根据原理 实现双向链表
"""

class Node(object):
    def __init__(self, value=None, pre=None, next=None):
        self._value = value
        self._pre = pre
        self._next = next

    def get_value(self):
        return self._value

    def get_pre(self):
        return self._pre

    def get_next(self):
        return self._next

    def set_value(self, value):
        self._value = value

    def set_pre(self, pre):
        self._pre = pre

    def set_next(self, next):
        self._next = next

    def has_pre(self):
        return self._pre is not None

    def has_next(self):
        return self._next is not None


class DoublyLinkedList(object):
    def __init__(self):
        self._head = None
        self._tail = None  # 尾部节点
        self._length = 0

    def is_empty(self):
        return self._head is None

    def get_length(self):
        return self._length

    def add(self, value):
        # add在链表前端添加元素
        new_node = Node(value)
        if not self._head:
            self._head = new_node
            self._tail = new_node
        else:
            new_node.set_next(self._head)
            self._head.set_pre(new_node)
            self._head = new_node
        self._length += 1

    def append(self, value):
        # append在链表尾部添加元素
        if self._length == 0:
            self.add(value)
        else:
            new_node = Node(value)
            new_node.set_pre(self._tail)
            self._tail.set_next(new_node)
            self._tail = new_node
        self._length += 1

    def search(self, value):
        # search检索元素是否在链表中 双向查找
        current_next = self._head
        current_pre = self._tail
        while 1:
            if current_next:
                if current_next.get_value() == value:
                    return True
                else:
                    current_next = current_next.get_next()
            if current_pre:
                if current_pre.get_value() == value:
                    return True
                else:
                    current_pre = current_pre.get_pre()
            if not current_pre and not current_next:
                return False

    def index(self, value):
        # index索引元素在链表中的位置 双向遍历
        current_pre = self._tail
        current_next = self._head
        end_index = self._length - 1
        index = 0
        while True:
            if current_pre:
                if current_pre.get_value() == value:
                    return end_index
                else:
                    end_index -= 1
                    current_pre = current_pre.get_pre()
            if current_next:
                if current_next.get_value() == value:
                    return index
                else:
                    index += 1
                    current_next = current_next.get_next()
            if not current_pre and not current_next:
                return -1

    def get(self, index):
        current_pre = self._tail
        current_next = self._head
        if index >= self._length:
            raise Exception("DoublyLinkedList index out of range.")
        pre_index = self._length - 1
        next_index = 0
        while current_next or current_pre:
            if current_next:
                if index == next_index:
                    return current_next.get_value()
                else:
                    next_index += 1
                    current_next = current_next.get_next()
            if current_pre:
                if index == pre_index:
                    return current_pre.get_value()
                else:
                    pre_index -= 1
                    current_pre = current_pre.get_pre()

    def remove(self, value):
        # remove删除链表中的某项元素
        current_node = self._head
        while current_node:
            if current_node.get_value() == value:
                pre_node = current_node.get_pre()
                next_node = current_node.get_next()
                if not pre_node:
                    next_node.set_pre(None)
                    self._head = next_node
                elif not next_node:
                    pre_node.set_next(None)
                    self._tail = pre_node
                else:
                    pre_node.set_next(next_node)
                    next_node.set_pre(pre_node)
                self._length -= 1
                break
            else:
                current_node = current_node.get_next()
                if not current_node:
                    raise Exception("Value %s is not found." % value)

    def insert(self, index, value):
        # insert链表中插入元素
        max_index = self._length - 1
        if index > max_index:
            self.append(value)
        elif index == 0:
            self.add(value)
        else:
            # 判断index离最左/最右哪个节点较近  从近的方向找
            if index < self._length // 2: # //除法不会四舍五入 而是直接舍弃
                current_node = self._head
                reverse = False
            else:
                current_node = self._tail
                reverse = True
            current_index = 0 if not reverse else max_index
            operate_1 = 'get_next()' if not reverse else 'get_pre()'
            while current_node:
                if eval("current_index == index"):
                    new_node = Node(value)
                    pre_node = current_node.get_pre()
                    new_node.set_pre(pre_node)
                    new_node.set_next(current_node)
                    pre_node.set_next(new_node)
                    current_node.set_pre(new_node)
                    self._length += 1
                    break
                else:
                    current_index = current_index + 1 if not reverse else current_index - 1
                    current_node = eval("current_node.%s" % operate_1)

    # def directional_traversal(self, reverse=False):
    #     """
    #     单向遍历 链表 所有元素
    #     :param reverse: 是否反向遍历 默认 否
    #     :return: list
    #     """
    #     pass

    # def bidirectional_traversal(self):
    #     # 双向遍历 链表 所有元素
    #     pass

    def clear(self):
        self._head = None
        self._tail = None
        self._length = 0

    def traversal(self, reverse=False):
        """
        遍历 链表
        :param reverse: 默认正向  True为反向结果
        :return: list
        """
        result = []
        current_node = self._head if not reverse else self._tail
        if self._length == 0:
            return result
        while current_node:
            result.append(current_node.get_value())
            if not reverse:
                current_node = current_node.get_next()
            else:
                current_node = current_node.get_pre()
        return result

    def show(self):
        # 打印元素
        head_node = self._head
        head_value_list = []
        tail_node = self._tail
        tail_value_list = []
        while head_node:
            value = str(head_node.get_value())
            head_value_list.append(value)
            head_node = head_node.get_next()
        while tail_node:
            value = str(tail_node.get_value())
            tail_value_list.append(value)
            tail_node = tail_node.get_pre()
        res = ['->'.join(head_value_list), '<-'.join(tail_value_list)]
        print(res)
        return res


if __name__ == '__main__':
    dll = DoublyLinkedList()
    print(dll.is_empty())
    dll.add(1)
    dll.add(2)
    dll.add(3)
    dll.append(9)
    dll.append(10)
    print(dll.get_length())
    dll.show()
    print(dll.search(9))
    print(dll.search(100))

    print("------------------------------")

    print(dll.index(10))
    print(dll.index(100))
    print(dll.get(4))
    # print(dll.get(5))

    print("------------------------------")

    # dll.remove(1)
    dll.remove(3)
    dll.remove(10)
    # dll.remove(100)
    dll.show()

    print("********************************")
    # dll.insert(1, 100)
    dll.insert(0, 0)
    dll.insert(5, 5)
    dll.insert(1, 3)
    dll.insert(5, 6)
    dll.show()

    print(dll.traversal())
    print(dll.traversal(True))

    print("********************************")
    dll.clear()
    print(dll.is_empty())