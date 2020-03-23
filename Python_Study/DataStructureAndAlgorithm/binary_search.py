#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 二分查找算法
:Author: 佳境Shmily
:Create Time: 2020/3/15 21:34
:File: binary_search
:Site: shmily-qjj.top
:Desc:
二分查找场景：寻找一个数、寻找左侧边界、寻找右侧边界。
"""
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# import sys
#
# sys.setrecursionlimit(9000000)


def binary_search(sorted_list, item, asc=True):
    """
    非递归的二分查找
    寻找一个数  如果存在，返回其索引值
    最基本的二分查找

    首先，假设表中元素是按升序排列，将表中间位置记录的关键字与查找关键字比较，如果两者相等，则查找成功；
    否则利用中间位置记录将表分成前、后两个子表，如果中间位置记录的关键字大于查找关键字，则进一步查找前一子表，否则进一步查找后一子表。
    重复以上过程，直到找到满足条件的记录，使查找成功，或直到子表不存在为止，此时查找不成功。

    :param asc: 默认认为传入的list是升序的  如果降序 需要反转
    :param sorted_list: 有序列表
    :param item: int 要找的元素
    :return: 找到了返回下标 否则返回-1
    """
    sorted_list = sorted_list if asc else list(reversed(sorted_list))
    low = 0  # 最小数的下标
    high = len(sorted_list)-1  # 最大数的下标
    n = 0  # 分的次数
    while low <= high:
        mid = (low + high) >> 1 if (low + high) % 2 == 1 else ((low + high) >> 1) + 1 # 精确获取中间值 下标
        n += 1
        if sorted_list[mid]==item:
            logger.info('二分法分了%s次，找到元素' % n)
            return mid
        if sorted_list[mid]<item:  # 要找的元素大于中间的 则从后半个list找
            low = mid + 1
        else:  # 要找的元素小于中间的 则从前半个list找
            high = (mid-1)
    logger.info('二分法分了%s次，未找到元素。' % n)
    return -1


def recursion_binary_search(sorted_list, start, end, item):
    """
    递归二分查找  查找有序数组的一个元素
    :param sorted_list: 有序数组  默认传升序数组
    :param start: 初始下标
    :param end: 结束下标
    :param item: 待查找元素
    :return: 如果找到，返回index  否则 -1
    """
    if start > end:  # 一定不能是大于等于 mid + 1等于end的时候很有可能mid+1就是找到的结果
        return -1
    # mid = (end + start) // 2  # 不四舍五入  得到中间元素
    mid = (start + end) >> 1 if (start + end) % 2 == 1 else ((start + end) >> 1) + 1  # 精确获取中间值 下标
    if sorted_list[mid] == item:
        return mid
    elif item > sorted_list[mid]:
        return recursion_binary_search(sorted_list, mid + 1, end, item)
    elif item < sorted_list[mid]:
        return recursion_binary_search(sorted_list, start, mid - 1, item)
    return -1



if __name__ == '__main__':
    m=[1,2,3,4,8,9,11,12,14,18,19,20,28,29]
    print(binary_search(m,20))
    m1 = [28, 20, 19, 18, 14, 12, 11, 9, 8, 4, 3, 2, 1]
    print(binary_search(m1,14,False))



    # #########################################################
    m=[1,2,3,4,8,9,11,12,14,18,19,20,28]
    print(recursion_binary_search(m, 0, len(m) - 1, 14))

