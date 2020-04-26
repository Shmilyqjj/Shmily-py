#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 剑指Offer 07
:Author: 佳境Shmily
:Create Time: 2020/4/26 10:40
:File: Solution07
:Site: shmily-qjj.top
大家都知道斐波那契数列，现在要求输入一个整数n，请你输出斐波那契数列的第n项（从0开始，第0项为0）。n<=39
"""

# -*- coding:utf-8 -*-
class Solution:
    # def Fibonacci(self, n):
    #     """
    #     递归 斐波那契
    #     :param n:
    #     :return:
    #     """
    #     if n == 0:
    #         return 0
    #     elif n == 1:
    #         return 1
    #     else:   # 从第三项开始  返回前两项的和  递归
    #         return self.Fibonacci(n-2) + self.Fibonacci(n-1)

    def Fibonacci(self, n):
        """
        非递归 斐波那契
        :param n:
        :return:
        """
        if n == 0:
            return 0
        if n == 1:
            return 1
        a = 0
        b = 1
        result = 0
        while n >= 2:
            result = a + b
            a = b
            b = result
            n -= 1
        return result





if __name__ == '__main__':
    s = Solution()
    print(s.Fibonacci(0))  # 0
    print(s.Fibonacci(1))  # 1
    print(s.Fibonacci(2))  # 1
    print(s.Fibonacci(3))  # 2
    print(s.Fibonacci(4))  # 3
    print(s.Fibonacci(5))  # 5