#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 05
:Author: 佳境Shmily
:Create Time: 2020/3/23 10:45
:File: Solution05
:Site: shmily-qjj.top


用两个栈来实现一个队列，完成队列的Push和Pop操作。 队列中的元素为int类型。
"""

# -*- coding:utf-8 -*-
class Solution:
    def __init__(self):
        self.stack1 = []  # 入队的栈
        self.stack2 = []  # 出队的栈

    def push(self, node):
        # write code here
        self.stack1.append(node)

    def pop(self):
        # return xx
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        return self.stack2.pop()


if __name__ == '__main__':
    s = Solution()
    s.push(1)
    s.push(2)
    s.push(3)

    print(s.pop())
    print(s.pop())
    print(s.pop())

    print("*************************************")

    # list的append相当于入栈  pop相当于出栈
    l = [1,2,3,4,5,6]
    print(l.pop())
    print(l.pop())
    print(l.pop())
    print(l.pop())
    print(l.pop())
