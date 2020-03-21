#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 其他公司 笔试编程题 及 实现
:Author: 佳境Shmily
:Create Time: 2020/3/22 0:18
:File: Solutions
:Site: shmily-qjj.top
"""
# def solution():
#     """
#     有一张包含n行m列的方格纸，每个小方格都是一个基地（总共有n*m个基地）
#     现在要放置补给品，如果补给品落在小方格内或边界上则该基地获得了补给品
#     如果补给点在交界处，则被视为已为交界的单元格都提供了补给品（如果在两个格子的边界上，则这两个都得到补给品，如果在四个格子中心点，这四个基地都得到补给品）
#     给定n，m，输出 最小要提供的补给品数量
#
#     例子：
#     2 2  得到：1
#     5 3  得到：6
#     :return:
#     """
#     input_str = input()
#     n, m = [int(x) for x in input_str.split(" ")]
#     if n * m <= 4:
#         print(1)
#         return
#
#     x_index = 0
#     y_index = 2
#     while True:
#         x_index += 1
#         if n % 2 == 0:
#             count = n >> 1
#         else:
#             count = (n >> 1) + 1
#         if x_index == n:
#             break
#     delta = count
#
#     while True:
#         if y_index % 2 == 1:
#             count += delta
#         if y_index == m:
#             break
#         y_index += 1
#     print(count)


def solution():
    pass


if __name__ == '__main__':
    solution()