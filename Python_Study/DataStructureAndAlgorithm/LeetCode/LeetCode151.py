#!/usr/bin/env python
# encoding: utf-8
"""
:Description: LeetCode 151. 翻转字符串里的单词
:Author: 佳境Shmily
:Create Time: 2020/4/30 23:29
:File: LeetCode151
:Site: shmily-qjj.top
题目：https://leetcode-cn.com/problems/reverse-words-in-a-string/
"""

class Solution:
    def reverseWords(self, s: str) -> str:
        return " ".join(s.split()[::-1])

if __name__ == '__main__':
    s = Solution()
    print(s.reverseWords(" a abbc  cd   dee   "))