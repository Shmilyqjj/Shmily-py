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


def binary_search(sorted_list, item, asc=True):
    """
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
        mid = int((low + high)/2)  # 中间值 下标
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

m=[1,2,3,4,8,9,11,12,14,18,19,20,28]
print(binary_search(m,14))

m1 = [28, 20, 19, 18, 14, 12, 11, 9, 8, 4, 3, 2, 1]
print(binary_search(m1,14,False))
