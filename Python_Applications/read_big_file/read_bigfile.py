#!/usr/bin/env python
# encoding: utf-8
"""
:Description:读取超大文件的最后几行
:Author: 佳境Shmily
:Create Time: 2020/4/14 15:45
:File: read_bigfile
:Site: shmily-qjj.top
"""

def read_bigfile(path):
    """
    倒数n个字符  倒数n行
    :param path:
    :return:
    """
    with open(path, "rb") as f:  # 必须rb模式否则无法从结尾读
        # f.seek(1000, 0)  # 移动指针到当前文件第1000个字节的位置
        # f.seek(1000, 1)  # 移动指针到相对当前位置之后的第1000个字节的位置
        f.seek(-10000, 2)  # 移动指针到相对文件结尾处之后的第-10000个字节的位置

        # f.read()  # 从seek指针位置开始往下读

        tmp = f.readlines()
        for i in range(-5, 0):   # 读倒数五行
            print(tmp[i])


def read_bigfile(path, lines):
    """
    倒数n行 预估每行字符数
    :param lines:结尾n行
    :param path:
    :return:
    """
    with open(path, "rb") as f:  # 必须rb模式否则无法从结尾读
        if not f:
            return

        f.seek(-lines * len(f.readlines(1)[0]) * 2, 2)  # 移动指针到相对文件结尾处之前的第（-2倍五行大概需要字节数）个字节的位置
        # f.read()  # 从seek指针位置开始往下读
        tmp = f.readlines()
        for i in range(-lines, 0):   # 读倒数五行
            print(tmp[i])



def count_lines(path):
    count = -1
    for count, line in enumerate(open(path, 'r')):
        pass
    count += 1
    print(count)

def count_lines1(path):
    count = 0
    f = open(path, "r")
    while True:
        res = f.read(8 * 1024 * 1024)
        if not res:
            break
        else:
            count += res.count("\n")
    print(count)


if __name__ == '__main__':
    # read_bigfile("d:\\GenerateLogs")
    read_bigfile("d:\\GenerateLogs", 8)
    count_lines("d:\\GenerateLogs")
    count_lines1("d:\\GenerateLogs")
