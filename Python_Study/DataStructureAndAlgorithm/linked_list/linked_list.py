#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 链表
:Author: 佳境Shmily
:Create Time: 2020/3/17 16:00
:File: linked_list
:Site: shmily-qjj.top

链表存储结构：地址可连续 也可 不连续

链表分为：单向链表 双向链表 循环链表

链表的基本元素有：
节点：每个节点有两个部分，左边部分称为值域，用来存放用户数据；右边部分称为指针域，用来存放指向下一个元素的指针。
head（头节点）:head节点永远指向第一个节点
tail（尾节点）: tail永远指向最后一个节点(tail为None)
None:链表中最后一个节点的指针域为None值
"""

class Node(object):
    """
    链表的节点  包含 值 和 右部分指针
    """
    def __init__(self, value=None, next=None):
        self._value = value
        self._next = next

    def get_value(self):
        return self._value

    def get_next(self):
        return self._next

    def has_next(self):
        return self._next is not None

    def set_value(self, value):
        self._value = value

    def set_next(self, next):
        self._next = next


class LinkedList(object):
    """
    单向链表
    """
    def __init__(self):
        # 初始化 为 空链表
        self._head = None
        self._size = 0

    def get_size(self):
        return self._size

    def is_empty(self):
        return self._head is None

    def add(self, value):
    # add在链表前端添加元素:O(1)
        new_node = Node(value, None)
        if self.is_empty():
            self._head = new_node
        else:
            new_node.set_next(self._head)
            self._head = new_node
        self._size += 1

    def append(self, value):
    # append在链表尾部添加元素:O(n)
        new_node = Node(value, None)
        if self.is_empty():
            # 如果为空 将添加的元素设置为第一个元素
            self._head = new_node
        else:
            # 不为空 从头节点开始遍历到尾部，添加到尾部
            current_node = self._head
            while current_node.has_next():
                current_node = current_node.get_next()
            current_node.set_next(new_node)
        self._size += 1

    def replace(self, index, value):
        current_node = self._head
        current_index = 0
        while current_node:
            if index == current_index:
                current_node.set_value(value)
                return True
            else:
                current_index += 1
                current_node = current_node.get_next()
        raise Exception("LinkedList index out of range.")

    def search(self, value):
    # search检索元素是否在链表中
        current_node = self._head
        while current_node.has_next():
            if current_node.get_value() == value:
                return True
            current_node = current_node.get_next()
        return False

    def index(self, value):
    # index索引元素在链表中的位置
    # 如果该值对应链表中多个位置 输出list
    # 如果不存在 输出-1
        index = 0
        result_list = []
        current_node = self._head
        while current_node.has_next():
            if current_node.get_value() == value:
                # return index
                result_list.append(index)
            if index == self._size - 1:
                break
            else:
                index += 1
                current_node = current_node.get_next()
        if result_list:
            return result_list
        else:
            return -1

    def get(self, index):
        current_node = self._head
        if index >= self._size:
            raise Exception('Linkedlist index out of range.')
        for i in range(self._size):
            if index == i:
                return current_node.get_value()
            else:
                current_node = current_node.get_next()

    def remove(self, value):
    # remove删除链表中的某项元素(只删除1个)
        success = False
        current_node = self._head
        current_index = 0
        pre_node = None
        while current_node.has_next():
            if current_node.get_value() == value:
                if not pre_node:
                    self._head = current_node.get_next()
                else:
                    pre_node.set_next(current_node.get_next())
                self._size -= 1
                success = True
                break
            else:
                pre_node = current_node
                current_node = current_node.get_next()
            current_index += 1
        return success

    def remove_multi(self, value):
        pass

    def insert(self, index, value):
    # insert链表中插入元素
        if index == 0 or self._size == 0:
            self.add(value)
        elif index >= self._size:
            self.append(value)
        else:
            new_node = Node(value)
            pre_node = None
            current_node = self._head
            pos = 0  # 位置
            while pos < index:
                pos += 1
                pre_node = current_node
                current_node = current_node.get_next()
            pre_node.set_next(new_node)
            new_node.set_next(current_node)
        self._size += 1

    def clear(self):
        """
        清空链表
        :return:
        """
        # i = self._size
        # while i:
        #     i -= 1
        #     need_delete_value = self.get(i)
        #     self.remove(need_delete_value)
        self._head = None
        self._size = 0

    def traversal(self, reverse=False):
        """
        遍历 链表
        :param reverse: 默认正向  True为反向结果
        :return: list
        """
        result = []
        current_node = self._head
        if self._size == 0:
            return result
        while current_node:
            result.append(current_node.get_value())
            current_node = current_node.get_next()
        if reverse:
            result = [result[i] for i in range(self._size-1, -1, -1)]
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
        # 打印元素
        if self._size == 0:
            return
        result_list = []
        current_node = self._head
        while current_node.has_next():
            node_value = current_node.get_value()
            result_list.append(node_value)
            current_node = current_node.get_next()
        result_list.append(current_node.get_value())
        result_list = [str(x) for x in result_list]
        print('->'.join(result_list))


if __name__ == '__main__':
    ll = LinkedList()
    print(1, ll.is_empty())
    ll.add(1)
    ll.add(2)
    ll.add(3)
    ll.add(4)

    ll.append(5)
    ll.append(5)

    ll.append(6)
    ll.append(5)
    ll.append(None)

    ll.insert(4, 4.444)

    print("remove 2", ll.remove(2))
    print("remove 7", ll.remove(7))
    ll.show()

    print("index 5", ll.index(5))
    print("index 10", ll.index(10))
    print("empty?", ll.is_empty())
    print("size?", ll.get_size())
    ll.show()

    print("search str 3", ll.search('3'))
    print("search 3", ll.search(3))
    print("search 103", ll.search('103'))
    print(ll.replace(4, 100))
    # print(ll.replace(10, 10000))
    print("-----------")

    ll.show()
    ll.reverse()
    ll.show()

    print("-----------")
    ll.show()
    print(ll.get(2))
    print(ll.traversal())
    print(ll.traversal(True))
    print("-----------")
    ll.show()
    print("remove 5--", ll.remove(5))
    print("index 5--", ll.index(5))
    ll.show()

    ll.clear()

    print("#######################")
    ll.add(1)
    ll.add(2)
    ll.add(2)
    ll.add(2)
    ll.add(2)
    ll.add(3)
    ll.show()
    ll.remove(2)
    ll.show()



