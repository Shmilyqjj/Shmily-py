#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 二分查找
:Author: 佳境Shmily
:Create Time: 2022/3/3 17:51
:File: BinarySearch
:Site: shmily-qjj.top
二分查找又称折半查找，优点是比较次数少，查找速度快，平均性能好；其缺点是要求待查表为有序表，且插入删除困难。因此，折半查找方法适用于不经常变动而查找频繁的有序列表。
首先，假设表中元素是按升序排列，将表中间位置记录的关键字与查找关键字比较，如果两者相等，则查找成功；否则利用中间位置记录将表分成前、后两个子表，如果中间位置记录的关键字大于查找关键字，则进一步查找前一子表，否则进一步查找后一子表。
重复以上过程，直到找到满足条件的记录，使查找成功，或直到子表不存在为止，此时查找不成功。

升序数组和一个数字 若数字在列表中 返回下标 若不在列表中，在保证升序的情况下返回插入数组的下标位置
[1,3,5,6],2 => 1
[1,3,5,6],5 => 2
"""

l = [1, 3, 5, 6, 7]
x = 3


def binary_search(alist, val):
    """
    递归二分查找 从alist中查找到val 找到返回True 找不到返回False
    :param alist: 数据列表
    :param val: 要查找的值
    :return:
    """
    n = len(alist)
    if n < 1:
        return False
    mid = n // 2
    if alist[mid] > val:
        return binary_search(alist[0:mid], val)
    elif alist[mid] < val:
        return binary_search(alist[mid+1:], val)
    else:
        return True


def bin_search(alist, val):
    """
    非递归二分查找 从alist中查找到val 找到返回True 找不到返回False
    :param alist: 数据列表
    :param val: 要查找的值
    :return:
    """
    n = len(alist)
    first = 0
    last = n - 1
    while first <= last:
        mid = (first + last) // 2
        if alist[mid] > val:
            last = mid - 1
        elif alist[mid] < val:
            first = mid + 1
        else:
            return True
    return False


if __name__ == '__main__':
    print(binary_search(l, x))
    print(bin_search(l, x))

