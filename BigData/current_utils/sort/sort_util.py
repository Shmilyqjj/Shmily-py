#!/usr/bin/env python
# encoding: utf-8
"""
:Description:排序工具 - 多种排序方法的封装
:Author: 佳境Shmily
:Create Time: 2020/3/14 21:04
:File: sort_util
:Site: shmily-qjj.top
:Tips:
1、稳定排序：如果 a 原本在 b 的前面，且 a == b，排序之后 a 仍然在 b 的前面，则为稳定排序。
2、非稳定排序：如果 a 原本在 b 的前面，且 a == b，排序之后 a 可能不在 b 的前面，则为非稳定排序。

3、原地排序：原地排序就是指在排序过程中不申请多余的存储空间，只利用原来存储待排数据的存储空间进行比较和交换的数据排序。
4、非原地排序：需要利用额外的数组来辅助排序。

5、时间复杂度：一个算法执行所消耗的时间。
6、空间复杂度：运行完一个算法所需的内存大小。

--> 稳定的排序：插入排序，冒泡排序，归并排序，计数排序，桶排序，基数排序
--> 不稳定的排序：选择排序，希尔排序，快速排序，堆排序

--> 复杂度为O(n2):选择排序，冒泡排序，插入排序
--> 复杂度为O(nlogn):快速排序，堆排序，归并排序

如果有序数列，快排时间复杂度为O(n2)
快排虽然快但是不稳定
既稳定又快的是归并排序
"""
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def bubble_sort(input, desc=False):
    """
    冒泡排序 - 稳定排序
    比较前后两个元素 交换
    1、时间复杂度：O(n2)  2、空间复杂度：O(1)  3、稳定排序  4、原地排序
    :param input: deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    """
    operate = '>' if desc else '<'
    input = deal_input(input)
    for i in range(len(input)):
        for j in range(len(input) - 1):
            if eval('input[i] %s input[j]' % operate):
                tmp = input[i]
                input[i] = input[j]
                input[j] = tmp
    return input


def new_bubble_sort(input, desc=False):
    """
    冒泡排序 - 稳定排序 优化版（减少排序次数）
    假如从开始的第一对到结尾的最后一对，相邻的元素之间都没有发生交换的操作，这意味着右边的元素总是大于等于左边的元素，此时的数组已经是有序的了，无需再对剩余的元素重复比较下去了。
    :param input: deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    """
    operate = '>' if desc else '<'
    input = deal_input(input)
    for i in range(len(input)):
        swap_flag = False  # 默认没发生交换
        for j in range(len(input) - 1):
            if eval('input[i] %s input[j]' % operate):
                swap_flag = True  # 如果这一趟有一次交换  flag置为True
                tmp = input[i]
                input[i] = input[j]
                input[j] = tmp
        if not swap_flag:
            break  # 如果这一趟没发生交换  说明已经有序 直接跳出
    return input


def select_sort(input, desc=False):
    """
    选择排序
    首先，找到数组中最小的那个元素，其次，将它和数组的第一个元素交换位置(如果第一个元素就是最小元素那么它就和自己交换)。其次，在剩下的元素中找到最小的元素，将它与数组的第二个元素交换位置。如此往复，直到将整个数组排序。
    1、时间复杂度：O(n2)  2、空间复杂度：O(1)  3、非稳定排序  4、原地排序
    :param input: deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    """
    operate = '>' if desc else '<'
    input = deal_input(input)
    for i in range(len(input)):
        index = i  # 从第一个元素遍历到最后一个元素
        for j in range(i, len(input)):  # 遍历剩下的元素
            if eval('input[j] %s input[index]' % operate):  # 如果 大于 或者 小于
                index = j  # 完成for循环后，找到 最大 或 最小 的元素 下标
        # 交换
        # 如果该元素就是最小元素，就跟自己交换
        tmp = input[i]
        input[i] = input[index]
        input[index] = tmp
    return input


def insert_sort(input, desc=False):
    """
    插入排序
    我们在玩打牌的时候，你是怎么整理那些牌的呢？一种简单的方法就是一张一张的来，将每一张牌插入到其他已经有序的牌中的适当位置。
    当我们给无序数组做排序的时候，为了要插入元素，我们需要腾出空间，将其余所有元素在插入之前都向右移动一位，这种算法我们称之为插入排序。
    1、时间复杂度：O(n2)  2、空间复杂度：O(1)  3、稳定排序  4、原地排序
    :param input:deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    过程：
    1、从数组第2个元素开始抽取元素。
    2、把它与左边第一个元素比较，如果左边第一个元素比它大，则继续与左边第二个元素比较下去，直到遇到不比它大的元素，然后插到这个元素的右边。
    3、继续选取第3，4，….n个元素,重复步骤 2 ，选择适当的位置插入。
    """
    operate = '>' if desc else '<'
    input = deal_input(input)
    length = len(input)
    if length == 0 or length < 2:
        return input
    for i in range(1,length):  # 下标从1开始(第二个元素开始)
        pre_index = i - 1 # 与当前元素比较的元素下标
        current_value = input[i]  # 当前元素值 这个元素与它之前的元素依次比较
        while pre_index >= 0 and eval('current_value %s input[pre_index]' % operate):
            # 当之前的元素大于当前元素则把之前的元素后移
            input[pre_index + 1] = input[pre_index]
            pre_index = pre_index - 1   # 得到需要插入的位置 要插入的位置为second_index + 1
        # 当比较元素小于当前元素，则将当前元素插入在 其后面
        input[pre_index+1] = current_value
    return input


def merge_sort_with_recursion(input, desc=False):
    """
    归并排序（递归方式）
    将一个大的无序数组有序，我们可以把大的数组分成两个，然后对这两个数组分别进行排序，之后在把这两个数组合并成一个有序的数组。
    由于两个小的数组都是有序的，所以在合并的时候是很快的。
    通过递归的方式将大的数组一直分割，直到数组的大小为 1，此时只有一个元素，那么该数组就是有序的了，之后再把两个数组大小为1的合并成一个大小为2的，再把两个大小为2的合并成4的 …
    直到全部小的数组合并起来。
    1、时间复杂度：O(nlogn)  2、空间复杂度：O(n)  3、稳定排序  4、非原地排序
    :param input:deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    """
    operate = '>=' if desc else '<='
    input = deal_input(input)
    def merge_sort(arr):
        """
        递归分治序列
        :param arr:
        :return:
        """
        if len(arr) <= 1:
            return arr
        num = len(arr) // 2   # /为浮点数除法   //为整数除法  5/2=2.5  5//2=2
        left = merge_sort(arr[:num])
        right = merge_sort(arr[num:])
        return merge(left, right)  # 合并

    def merge(left, right):
        """
        合并操作
        :param left: 左子集合
        :param right:右边子集合
        :return:
        """
        l, r = 0, 0  # 初始化index
        result = []
        while l < len(left) and r < len(right):
            if eval("left[l] %s right[r]" % operate):  # 筛选排序将left与right最小元素按序加入新序列
                result.append(left[l])
                l += 1
            else:
                result.append(right[r])
                r += 1
        result += left[l:]
        result += right[r:]
        return result
    return merge_sort(input)


def merge_sort_without_recursion(input, desc=False):
    """
    归并排序（非递归方式）
    非递归  首先划分每个子数组元素的个数（也就是子数组的长度)->求出low，mid，high->对每个相邻的数组进行排序合并->
    1、时间复杂度：O(nlogn)  2、空间复杂度：O(n)  3、稳定排序  4、非原地排序
    :param input:deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    :References:https://www.jianshu.com/p/3f27384387c1
    """
    operate = '>=' if desc else '<='
    input = deal_input(input)

    # 归并排序都是先确定low mid high，等确定了，就可以merge了
    def merge(arr, low, mid, height):
        """
        合并操作
        :param left: 左子集合
        :param right:右边子集合
        :return:
        """
        left = arr[low:mid]
        right = arr[mid:height]
        l, r = 0, 0  # 初始化index
        result = []
        while l < len(left) and r < len(right):
            if eval("left[l] %s right[r]" % operate):  # 筛选排序将left与right最小元素按序加入新序列
                result.append(left[l])
                l += 1
            else:
                result.append(right[r])
                r += 1
        result += left[l:]
        result += right[r:]
        arr[low: height] = result
        return result

    # 获取low mid height的过程：
    i = 1  # 首先设置子数组长度为1
    result = []
    while i < len(input):
        logger.info("子数组长度：%s" % i)
        # 求得要合并的两个相邻数组的区间 [low:mid) [mid:height)
        # 求得通用公式：
        # low = low + 2 x i
        # mid = low + i
        # height = low + 2 x i
        low = 0  # 初始化low index
        while low < len(input):
            mid = low + i
            height = low + 2 * i if low + 2 * i <= len(input) else len(input)  # 防止height下标越界
            if mid < height: # 防止mid下标越界
                logger.info("low:%s  mid:%s  height:%s" % (low, mid, height))
                result = merge(input, low, mid, height)
            low += i * 2
        i = i * 2    # 子数组长度 每次递增两倍
    return result


def shell_sort(input, desc=False):
    """
    希尔排序
    :param input:deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    """
    operate = '>' if desc else '<'
    input = deal_input(input)


def quick_sort(input, desc=False):
    """
    快速排序
    1.选择一个中轴元素
    2.然后把数组中所有小于中轴元素的元素放在其左边，所有大于或等于中轴元素的元素放在其右边
    此时中轴元素所处的位置的是有序的，无需再移动中轴元素的位置
    3.从中轴元素那里开始把大的数组切割成两个小的数组(两个数组都不包含中轴元素)
    4.接着通过递归的方式，让中轴元素左边的数组和右边的数组也重复同样的操作，直到数组的大小为1，此时每个元素都处于有序的位置

    1、时间复杂度：O(nlogn)  2、空间复杂度：O(logn)  3、非稳定排序  4、原地排序
    :param input:deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    """
    operate = '>' if desc else '<'
    input = deal_input(input)



def heap_sort(input, desc=False):
    """
    堆排序
    :param input:deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    """
    operate = '>' if desc else '<'
    input = deal_input(input)


def count_sort(input, desc=False):
    """
    计数排序
    :param input:deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    """
    operate = '>' if desc else '<'
    input = deal_input(input)


def bucket_sort(input, desc=False):
    """
    桶排序
    :param input:deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    """
    operate = '>' if desc else '<'
    input = deal_input(input)


def base_sort(input, desc=False):
    """
    基数排序
    :param input:deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    """
    operate = '>' if desc else '<'
    input = deal_input(input)


def builtin_sort(input, desc=False):
    """
    python内建排序
    :param input: deal_input支持的格式
    :param desc: 默认False 默认不降序，默认升序
    :return: list
    """
    input = deal_input(input)
    return sorted(input,reverse=desc)


def deal_input(input, dict_flag='key'):
    """
    输入格式统一处理
    :param input: input类型为list set tuple dict str  输出为list 供排序用
    :param dict_flag: dict_flag 如果传入input为dict dict_flag决定输出key或value列表
    :return: list
    """
    if isinstance(input, list):
        return input
    elif isinstance(input, set):
        return list(input)
    elif isinstance(input, tuple):
        return list(tuple)
    elif isinstance(input, dict):
        if dict_flag == 'key':
            return list(input)
        else:
            return list(input.values())
    elif isinstance(input, str):
        result = []
        for i in input:
            if i not in [str(x) for x in range(10)]:
                i = ord(i)  # 转ASCII码
            else:
                i = int(i)
            result.append(i)
        return result


if __name__ == '__main__':
    input = [10,5,6,2,8,1,3,7,4,9]
    # print(bubble_sort(input))
    # print(new_bubble_sort(input))
    # print(select_sort(input))
    # print(insert_sort(input))
    # print(merge_sort_with_recursion(input))
    print(merge_sort_without_recursion(input))

    # print(insert_into_specified_location(input,10,2.5))

    # print(builtin_sort(input))
