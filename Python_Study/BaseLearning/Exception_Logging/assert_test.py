# -*- coding:utf-8 -*-
"""
:Description: python3 assert断言  在表达式不成立时抛异常
:Owner: Shmily qjj
:Create time: 2020/08/24 10:17
"""


def f1():
    assert 1 == 2
    # 等价于
    if not 1 == 2:
        raise AssertionError


def f2():
    assert 1 == 2, "1 != 2"
    # 等价于
    if not 1 == 2:
        raise AssertionError("1 != 2")

if __name__ == '__main__':
    f2()