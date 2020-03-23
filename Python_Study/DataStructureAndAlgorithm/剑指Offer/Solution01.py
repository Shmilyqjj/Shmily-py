#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 01
:Author: 佳境Shmily
:Create Time: 2020/3/23 9:22
:File: Solution01
:Site: shmily-qjj.top


在一个二维数组中（每个一维数组的长度相同），每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。
请完成一个函数，输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。
"""

class Solution:
    # array 二维列表
    def Find(self, target, array):
        # write code here
        n = len(array[0])
        if n == 0:
            return False
        for x_list in array:
            if x_list[n-1] < target:
                continue
            for x in x_list:
                if target == x:
                    return True
        return False



if __name__ == '__main__':
    s = Solution()
    print(s.Find(15, [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]))
    print(s.Find(15, [[]]))