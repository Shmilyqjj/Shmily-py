#!/usr/bin/env python
# encoding: utf-8
"""
:Description:
:Author: 佳境Shmily
:Create Time: 2020/3/23 7:32
:File: Solution1
:Site: shmily-qjj.top
"""

# def solution():
#     """
#     正在挑战一个CrackMe的你，把需要填写的前面几位密码都正确猜出了，可是这最后一位密码，好像藏得有点深。
#     CrackMe的作者还挑衅般的在里面藏了个.tar.gz文件，解压缩出来，里面写道 你要的最后一个字符就在下面这个字符串里，这个字符是下面整个字符串中第一个只出现一次的字符。
#     （比如，串是abaccdeff，那么正确字符就是b了） 然而下面给出来的字符串好像太长太长了，单靠人力完全无法找出来。 于是，你需要写一个程序代劳了。
#     输入文件体积较大，请使用一些快速的输入输出手段，不推荐使用cin/cout，对Java并不推荐使用Scanner直接读写。
#
#     第一行，一个正整数T(T≤20)  ，表示输入数据组数。
#     之后T行，每行一个字符串S。( 1≤S  的长度≤1000000   ，保证字符串中出现的字符的ASCII码在[0x21,0x7F)范围内，即均为可显示的非空白符，同时保证一定有解)
#
#     输入：一共T行，每行一个字符C ，表示所给的相应字符串中第一个只出现一次的字符。
#
#     例子：
#     2
#     abaccdeff
#     testonline
#
#     输出
#     b
#     s
#     :return:
#     """
#     line_num = int(input())
#     black_list = []
#     stack = []
#     while line_num:
#         in_str = input()
#         for s in in_str:
#             if not stack.__contains__(s) and s not in black_list:
#                 stack.append(s)
#             elif stack.__contains__(s):
#                 stack.remove(s)
#                 black_list.append(s)
#         line_num -= 1
#         print(stack[0])
#         stack.clear()
#         black_list.clear()


def solution():
    pass


if __name__ == '__main__':
    solution()