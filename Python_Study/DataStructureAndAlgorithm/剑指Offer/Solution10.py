#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 10  矩阵覆盖
:Author: 佳境Shmily
:Create Time: 2020/4/26 11:48
:File: Solution10
:Site: shmily-qjj.top
题目描述
我们可以用2*1的小矩形横着或者竖着去覆盖更大的矩形。请问用n个2*1的小矩形无重叠地覆盖一个2*n的大矩形，总共有多少种方法？

找规律 得到：
n: 1 2 3 4
=> 1 2 3 5
规律是斐波那契
"""


class Solution:
    def rectCover(self, number):
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
    print(s.rectCover(0))
    print(s.rectCover(1))
    print(s.rectCover(2))
    print(s.rectCover(3))
    print(s.rectCover(4))
    print(s.rectCover(5))
