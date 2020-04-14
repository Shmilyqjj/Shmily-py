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


def linecache_test(path):
    """
该模块允许从任何文件里得到任何的行，并且使用缓存进行优化，常见的情况是从单个文件读取多行。

linecache.getlines(filename)
从名为filename的文件中得到全部内容，输出为列表格式，以文件每行为列表中的一个元素,并以linenum-1为元素在列表中的位置存储

linecache.getline(filename,lineno)
从名为filename的文件中得到第lineno行。这个函数从不会抛出一个异常–产生错误时它将返回”（换行符将包含在找到的行里）。
如果文件没有找到，这个函数将会在sys.path搜索。

linecache.clearcache()
清除缓存。如果你不再需要先前从getline()中得到的行

linecache.checkcache(filename)
检查缓存的有效性。如果在缓存中的文件在硬盘上发生了变化，并且你需要更新版本，使用这个函数。如果省略filename，将检查缓存里的所有条目。

linecache.updatecache(filename)
更新文件名为filename的缓存。如果filename文件更新了，使用这个函数可以更新linecache.getlines(filename)返回的列表。
    :param path:
    :return:
    """
    import linecache
    pass

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
    # count_lines1("d:\\GenerateLogs")
    # linecache_test("d:\\GenerateLogs")