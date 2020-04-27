#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 12
:Author: 佳境Shmily
:Create Time: 2020/4/26 11:59
:File: Solution12
:Site: shmily-qjj.top
给定一个double类型的浮点数base和int类型的整数exponent。求base的exponent次方。
保证base和exponent不同时为0
"""

class Solution:
    # def Power(self, base, exponent):
    # 调用函数
    #     # write code here
    #     return base ** exponent

    # def Power(self, base, exponent):
    # 调用函数
    #     # write code here
    #     return pow(base, exponent)

    def Power(self, base, exponent):
    # 不调用函数
        # write code here
        result = 1
        if base == 0:
            return 0
        elif exponent == 0:
            return 1
        elif exponent > 0:
            while exponent:
                result *= base
                exponent -= 1
            return result
        else:
            while exponent:
                result /= base
                exponent += 1
            return result


if __name__ == '__main__':
    s = Solution()
    print(s.Power(2.5, 2))
    print(s.Power(-2.5, 2))
    print(s.Power(-2.5, -2))