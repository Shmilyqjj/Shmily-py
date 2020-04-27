#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 13
:Author: 佳境Shmily
:Create Time: 2020/4/26 11:59
:File: Solution13
:Site: shmily-qjj.top
输入一个整数数组，实现一个函数来调整该数组中数字的顺序，使得所有的奇数位于数组的前半部分，所有的偶数位于数组的后半部分，并保证奇数和奇数，偶数和偶数之间的相对位置不变。

相对位置不变 ==> 稳定的
"""


class Solution:
    # def reOrderArray(self, array):
    # 解法1  分类奇数偶数 再相加
    #     # write code here
    #     odd, even = [], []  # odd奇数  even偶数
    #     for i in array:
    #         odd.append(i) if i % 2 == 1 else even.append(i)
    #     return odd + even

    def reOrderArray(self, array):
        # write code here
        # 解法2
        return sorted(array, key=lambda x: x%2, reverse=True)


if __name__ == '__main__':
    s = Solution()
    print(s.reOrderArray([1, 2, 3, 4, 5, 6, 7, 8, 7, 9, 10]))

