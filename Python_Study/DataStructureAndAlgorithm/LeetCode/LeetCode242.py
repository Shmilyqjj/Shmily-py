#!/usr/bin/env python
# encoding: utf-8
"""
:Description: LeetCode 242. 有效的字母异位词
:Author: 佳境Shmily
:Create Time: 2020/4/30 14:10
:File: LeetCode242
:Site: shmily-qjj.top

题目：https://leetcode-cn.com/problems/valid-anagram/
"""

class Solution:
    # def isAnagram(self, s: str, t: str) -> bool:
    #     return sorted(s) == sorted(t)   # 一行搞定

    def isAnagram(self, s: str, t: str) -> bool:
        flag = True
        if not len(set(s)) == len(set(t)):
            return False
        for i in set(t):
            if s.count(i) != t.count(i):
                flag = False
        return flag


if __name__ == '__main__':
    s = Solution()
    print(s.isAnagram("anagram", "nagaram"))
    print(s.isAnagram("a", "ab"))