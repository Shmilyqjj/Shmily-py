#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 11
:Author: 佳境Shmily
:Create Time: 2020/4/27 11:50
:File: Solution11
:Site: shmily-qjj.top
输入一个整数，输出该数二进制表示中1的个数。其中负数用补码表示。

注：正数的原码=反码=补码（正数的原码、反码、补码是一致的）   负数的补码是反码加1，反码是对原码按位取反，只是最高位(符号位)不变   算机数字运算均是基于补码的


127的反码为0111 1111
-127的反码为1000 0000
127的补码为0111 1111
-127的补码为1000 0001
00000000 00000000 00000000 00000101 是 5的原码
10000000 00000000 00000000 00000101 是-5的原码

（1）正数的补码与原码相同；
（2）负数的符号位为1，其余位为该数绝对值的原码按位取反，然后整个数加1，即为其补码。
"""


class Solution:
    def NumberOf1(self, n):
        # write code here
        if n<0:
            n = n&0xffffffff   # 1111 1111 1111 1111 1111 1111 1111 1111 (8个F的二进制形式, 一个F占4个字节)
        return bin(n).count("1")  # 十进制转二进制 带正负




if __name__ == '__main__':
    s = Solution()
    print(s.NumberOf1(1))
    print(s.NumberOf1(2))
    print(s.NumberOf1(8))
    print(s.NumberOf1(64))
    print(s.NumberOf1(-1))
    print(s.NumberOf1(-100))
