#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 09
:Author: 佳境Shmily
:Create Time: 2020/4/26 11:46
:File: Solution09
:Site: shmily-qjj.top
上一题的变形
一只青蛙一次可以跳上1级台阶，也可以跳上2级……它也可以跳上n级。求该青蛙跳上一个n级的台阶总共有多少种跳法。

也是找规律
参考：https://www.jianshu.com/p/965d12083d7f
最终得到公式：f(n) = 2^(n-1)

考点贪心：https://baijiahao.baidu.com/s?id=1642122740570394361&wfr=spider&for=pc
"""
class Solution:
    def jumpFloorII(self, number):
        # write code here
        if number == 0:
            return 0
        if number == 1:
            return 1
        return 2 ** (number-1)  # **是乘方


if __name__ == '__main__':
    s = Solution()
    print(s.jumpFloorII(0))
    print(s.jumpFloorII(1))
    print(s.jumpFloorII(2))
    print(s.jumpFloorII(3))
