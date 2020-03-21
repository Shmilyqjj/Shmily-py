#!/usr/bin/env python
# encoding: utf-8
"""
:Description:栈 学习
:Author: 佳境Shmily
:Create Time: 2020/3/17 15:27
:File: stack
:Site: shmily-qjj.top

栈的特点是后进先出（LIFO），队列的特点是先进先出（FIFO）

stack和queue是不能通过查询具体某一个位置的元素而进行操作的。但是他们的排列是按顺序的
对于stack我们可以使用python内置的list实现，因为list是属于线性数组，在末尾插入和删除一个元素所使用的时间都是O(1),这非常符合stack的要求。
当然，我们也可以使用链表来实现。

线性表的两种存储：顺序存储和链式存储
顺序存储结构：用一段地址连续的存储单元依次存储线性表的数据元素
链式存储结构：地址可以连续也可以不连续的存储单元存储数据元素

"""


class Stack(object):
    """
    基于python list实现 栈
    """
    def __init__(self, init_stack = None):
        self.stack = init_stack if init_stack else []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            raise Exception("Empty Stack.")

    def is_empty(self):
        return bool(self.stack)

    def get_top(self):
        if self.stack:
            return self.stack[len(self.stack)-1]
        else:
            raise Exception("Empty Stack.")

# ######################################################################################################################
"""
基于LinkedList实现栈
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

    def has_next(self):
        return self._next is not None


class LinkedListStack(object):
    """
    基于 链表 实现 栈
    """
    def __init__(self):
        self._stack_top = None  # 栈顶
        self._stack_bottom = None  # 栈底
        self._size = 0

# 的插入和删除操作只允许在表的一端进行
    def push(self, value):
        new_node = Node(value)
        if not self._stack_top:
            self._stack_top = new_node
            self._stack_bottom = new_node
        else:
            new_node.set_next(self._stack_top)
            self._stack_top = new_node
        self._size += 1

    def pop(self):
        if self._stack_top:
            top_value = self._stack_top.get_value()
            self._stack_top = self._stack_top.get_next()
        else:
            raise Exception("Stack is empty.")
        return top_value

    def is_empty(self):
        if self._stack_top:
            return False
        else:
            return True

    def get_top(self):
        return self._stack_top.get_value()

    def search(self, element):
        """
        在堆栈中搜索element如果存在，则返回它相对于栈顶的偏移量。否则，返回-1。
        :return:
        """
        if self.is_empty():
            return -1
        current_node = self._stack_top
        current_index = 0
        while current_node:
            if current_node.get_value() == element:
                return current_index
            current_node = current_node.get_next()
            current_index += 1
        return -1

    def get_size(self):
        return self._size

    def clear(self):
        self.__init__()

    def show(self):
        current_node = self._stack_top
        result_list = []
        while current_node:
            result_list.append(current_node.get_value())
            current_node = current_node.get_next()
        result_list = [str(x) for x in result_list]
        print("栈顶 " + '->'.join(result_list) + " 栈底")


if __name__ == '__main__':
    ll_stack = LinkedListStack()
    ll_stack.push(1)
    ll_stack.push(2)
    ll_stack.push(3)
    ll_stack.push(4)
    print(ll_stack.get_size())
    ll_stack.show()
    print(ll_stack.get_top())
    print("***********************")
    # print(ll_stack.pop())
    # print(ll_stack.pop())
    # print(ll_stack.pop())
    # print(ll_stack.pop())
    # print(ll_stack.is_empty())
    # ll_stack.show()
    ll_stack.show()
    print(ll_stack.search(10))
    print(ll_stack.search(3))
