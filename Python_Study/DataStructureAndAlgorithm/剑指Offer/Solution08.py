#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 08
:Author: 佳境Shmily
:Create Time: 2020/4/26 11:45
:File: Solution08
:Site: shmily-qjj.top
一只青蛙一次可以跳上1级台阶，也可以跳上2级。求该青蛙跳上一个n级的台阶总共有多少种跳法（先后次序不同算不同的结果）。

思路：找规律列函数
规律就是斐波那契
n:  0 1 2 3 4...
=>: 0 1 2 3 5...

如果用递归  可能会超过最大递归深度
所以用非递归的斐波那契
f(n) = f(n-1) + f(n-2)
"""


class Solution:
    def jumpFloor(self, number):
        # write code here
        if not number:
            return 0
        elif number == 1:
            return 1
        elif number == 2:
            return 2
        else:
            a = 1
            b = 2
            result = 0
            while number > 2:
                result = a + b
                a = b
                b = result
                number -= 1
            return result

if __name__ == '__main__':
    s = Solution()
    print(s.jumpFloor(0))
    print(s.jumpFloor(1))
    print(s.jumpFloor(2))
    print(s.jumpFloor(3))
    print(s.jumpFloor(4))
    print(s.jumpFloor(5))
