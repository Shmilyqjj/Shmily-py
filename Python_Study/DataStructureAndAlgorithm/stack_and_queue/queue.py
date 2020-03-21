#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 队列 queue
:Author: 佳境Shmily
:Create Time: 2020/3/17 15:27
:File: queue
:Site: shmily-qjj.top
栈的特点是后进先出（LIFO），队列的特点是先进先出（FIFO）

队列的基本方法
count：获取Queue中包含的元素个数
clear()：从Queue中移除所有的元素
contains(object obj)：判断某个元素是否在Queue中
Dequeue()：移除并返回在Queue的开头的对象
Enqueue(object obj)：向Queue的末尾添加一个对象
ToArray()：赋值Queue到一个新的数组中
TrimToSize()：设置容量为Queue中元素的实际个数

队列分 顺序队列 和 链式队列
"""

class Node(object):
    def __init__(self, value):
        self._value = value
        self._next = None

    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def set_next(self, next_node_obj):
        self._next = next_node_obj

    def get_next(self):
        return self._next

    def has_next(self):
        return self._next is not None


class Queue(object):
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def count(self):
        return self._size

    def enqueue(self, value):
        new_node = Node(value)
        if not self._head:
            self._head = new_node
            self._tail = new_node
        else:
            new_node.set_next(self._head)
            self._head = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("Empty Queue.")
        elif self._size == 1:
            result = self._tail.get_value()
            self._head = self._tail = None
            self._size -= 1
            return result
        else:
            result = None
            current_node = self._head
            while current_node:
                if current_node.get_next() == self._tail:
                    current_node.set_next(None)
                    result = self._tail.get_value()
                    self._tail = current_node
                    break
                else:
                    current_node = current_node.get_next()
            self._tail = current_node
            self._size -= 1
            return result

    def is_empty(self):
        return self._size == 0

    def get_top(self):
        # 获取 最早入队的元素
        if not self.is_empty():
            return self._tail.get_value()

    def clear(self):
        self.__init__()

    def contains(self, value):
        current_node = self._head
        while current_node:
            if current_node.get_value() == value:
                return True
            else:
                current_node = current_node.get_next()
        return False

    def to_array(self):
        current_node = self._head
        result = []
        while current_node:
            result.append(current_node.get_value())
            current_node = current_node.get_next()
        return result

    def show(self):
        if self.is_empty():
            return
        current_node = self._head
        result_list = []
        while current_node:
            result_list.append(str(current_node.get_value()))
            if current_node.has_next():
                current_node = current_node.get_next()
            else:
                break
        print("队头 " + "->".join(result_list) + " 队尾")


def queue():
    """
    基于Python的List实现队列
    队列 先进先出 FIFO
    队列在队头做删除操作,在队尾做插入操作
    插入元素 0 1 2 3 4 5
    :return:
    """
    queue = [1, 2, 3, 4, 5, 6]
    print("queue:", queue)
    queue.insert(0, 0)  # 入队enqueue  在index=0的位置插入0
    queue.insert(0, -1)  # 在index=0的位置插入1
    queue.insert(0, -2)
    print("enqueue后的queue:", queue)
    while queue:
        o = queue.pop()
        print("pop:", o)

if __name__ == '__main__':
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    print(q.count())
    q.show()
    print(q.get_top())
    print(q.contains(0))

    print("-***********************-")
    print(q.to_array())

    print(q.dequeue())
    q.show()
    print(q.dequeue())
    q.show()
    print(q.dequeue())
    q.show()
    print(q.count())

    print("####################################################")
    queue()