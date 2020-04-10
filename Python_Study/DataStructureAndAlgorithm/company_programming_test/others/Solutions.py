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


# def solution():
#     """
#     给定一个字符串数组A 字符串由小写英文字母组成，每个字符串长度相同。现在对于每个字符串，要删除几个相同索引的字符，假定删除字符的索引集合为D，
#     使得删除字符后字符串数组按照字典序排序，并且希望每个字符串删除的字符数量最小，请给出相应的最小值。
#     :return:
#     """
#     A=[]
#     A=["xc", "yb", "za"]  # 0  说明：这个已经按字典序排序了所以 D=[]
#     A=["ca", "bb", "ac"]  # 1  说明：每个字符串索引0分别是c,b,a 可删除索引为0的字符 D=[0] 删除后["a","b","c"]字典序了
#     A=["zyx", "wvu", "tsr"]  # 3  说明：必须全部删掉 D=[0,1,2]
#     if not A:
#         return 0
#     D = []
#     for i in range(len(A[0])):
#         flag = False
#         tmp = 0
#         for s in A:
#             if not flag:
#                 tmp = ord(s[i])
#                 flag = True
#                 continue
#             else:
#                 if ord(s[i]) - 1 != tmp:
#                     D.append(i)
#                     break
#                 else:
#                     tmp = ord(s[i])
#     print(len(D))


# def solution():
#     """
#     对给定数组A，如果i<j且A[i] <= A[j]则称(i,j)为正序对，j-i为正序对的宽度，求正序对A的最大宽度
#     :return:
#     """
#     A=[]
#     A=[6,0,8,2,1,5]  # 4
#     A=[1,0,8,2,1,7]  # 5
#     A=[8,0,8,2,1,7]  # 4
#     A=[0,1]  # 1
#     A=[10, 9, 8, 7, 6, 5, 1, 9]   # 6
#     if not A or len(A) == 1:
#         return 0
#     else:
#         length = 0
#         for i in range(len(A)):
#             tmp = 0
#             for j in range(i, len(A)):
#                 if A[j] - A[i] >= 0 and j - i > tmp:
#                     tmp = j - i
#             if tmp > length:
#                 length = tmp
#         print(length)


def solution():
    """
    给定一系列数字要求数字重量从小到大排序
    重量：每一位上的数字求和即为重量 19的重量1+9=10
    按数字重量从小到大排序，重量相等时按字典序  字典序 使用python的sorted可以实现sorted(l,key=str)
    :return:
    """
    input = ["71899703","425","81","91","9","18","7","7","6","72","27","7516","7615","821","812"]
    input = ["71899703","18","9","81","7","7","7516","7615","821","812"]
    # input = ["81","9","18","27","72"]
    tmp_dict = {}
    for i in range(len(input)):
        weight = 0
        single_value = input[i]
        for idx in range(len(single_value)):
            s = single_value[idx]
            weight += int(s)
        tmp_dict.setdefault(weight, []).append(single_value)
    tmp_dict = {x[0]:x[1] for x in sorted(tmp_dict.items(), key=lambda x: x[0])}
    print(tmp_dict)
    result_list = []
    for t in tmp_dict:
        l = tmp_dict[t]
        if len(l) == 1:
            result_list.append(l[0])
        else:
            result_list.extend(sorted(l,key=str))
    return result_list

if __name__ == '__main__':
    print(solution())