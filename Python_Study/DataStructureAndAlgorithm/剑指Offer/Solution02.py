#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 02
:Author: 佳境Shmily
:Create Time: 2020/3/23 9:36
:File: Solution02
:Site: shmily-qjj.top

请实现一个函数，将一个字符串中的每个空格替换成“%20”。例如，当字符串为We Are Happy.则经过替换之后的字符串为We%20Are%20Happy。
"""


class Solution:
    # s 源字符串
    def replaceSpace(self, s):
        # write code here
        return s.replace(" ", "%20")


if __name__ == '__main__':
    s = Solution()
    print(s.replaceSpace("We Are Happy."))