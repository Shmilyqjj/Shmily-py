#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 美团2020春招 笔试
:Author: 佳境Shmily
:Create Time: 2020/4/16 19:02
:File: Solution01
:Site: shmily-qjj.top
五道题全做了，自测答案对但AC率不高。。。誒。。。
"""

def solution01():
    """
    某学校的期末考试共有n个学生参加，考试科目共有m科。学校将会给一部分学生颁发单科成绩优秀奖，获奖学生需要满足的条件是某一科的成绩是所有学生中最高的或是最高的之一。请问学校应该给多少名学生颁发单科成绩优秀奖。

输入
输入第一行包含两个正整数n和m，分别代表学生人数和考试科目数量。(n,m<=500)

接下来有n行，每行有m个正整数，每个正整数在1-100之间，中间用空格隔开，表示每个学生的m科考试成绩。

输出
输出仅包含一个整数，表示获得单科成绩优秀奖的人数


样例输入
5 5
28 35 38 10 19
4 76 72 38 86
96 80 81 17 10
70 64 86 85 10
1 93 19 34 41
样例输出
4

提示
注意，输出结果为人数，并非人次。同一个学生如有多科最优，获奖人数也只会计为1人，即输出结果始终小于等于n
    :return:
    0%
    """
    n = 5
    m = 5
    s_dict = {0: [28, 35, 38, 10, 19], 1: [4, 76, 72, 38, 86], 2: [96, 80, 81, 17, 10], 3: [70, 64, 86, 85, 10], 4: [1, 93, 19, 34, 41]}
    # n, m = [int(x) for x in input().split(" ")]
    # s_dict = {}
    # s_id = 0
    # for i in range(n):
    #     s_dict[s_id] = [int(x) for x in input().split(" ")]
    #     s_id += 1
    good_stu_list = []
    for j in range(m):
        score_list = []
        for s_id in range(n):
            score_list.append([s_id, s_dict[s_id][j]])
        score_list = sorted(score_list, key=lambda x: x[1])
        print(score_list)
        good_stu_list.append(score_list[-1:][0][0])

    print(len(set(good_stu_list)))


def solution02():
    """
    题目描述：
有这么一段伪代码

input a,b,m,x

while true:

  x=(a*x+b)%m

  print(x)

end while

输出的x由于是在取模意义下的，所以会出现循环。

比如，a=2, b=1, m=5, x=2的时候，输出的序列将会如下：

0,1,3,2,0,1,3,2,0,1,3,2....

其中：0,1,3,2 称为最短的循环节。

现在给定a,b,m,x的值，请你计算最短循环节的长度。

输入
输入4个数，a,b,m,x

输出
输出一个数，最短循环节的长度


样例输入
2 1 5 2
样例输出
4

提示
1≤a,b,x≤m≤100000 ,a,b,x,m均为正整数
    :return:
    18%
    """
    a, b, m, x = [int(x) for x in input().split(" ")]
    limit = 100
    count = 0
    out = []
    while count <= limit:
        x = (a * x + b) % m
        out.append(str(x))
        count += 1
    print(len(set(out)))



def solution03():
    """
    题目描述：
数对是数学中一个重要的概念，类似于计算机中的pair，数对的性质如下：

每个数对(x,y)包含两个实数元素x,y，描述一对数之间的关系。两个数对比大小将先比较第一个数的大小，如果相同再比较第二个数的大小。

现在，有n个数（两两可能相同），他们之间两两将会形成n^2个数对（自己和自己也会形成数对）。我们希望知道，第k小的数对是哪一对数，并输出这一对。

输入
第一行包含两个数n,k，含义如题面所示

接下来一行n个整数，空格隔开。

输出
输出第k小的数对。格式如(x,y)，其中x为数对中第一个数，y为数对中第二个数


样例输入
3 4
3 1 2
样例输出
(2,1)

提示
n≤100000,1≤k≤n^2，这n个数在int范围内[-2147483648,2147483647]

样例解释
数对一共有9个，分别是： (3,3)(3,1)(3,2)(1,3)(1,1)(1,2)(2,3)(2,1)(2,2)
按从小到大的排序后：(1,1)(1,2)(1,3)(2,1)(2,2)(2,3)(3,1)(3,2)(3,3)
第4个为(2,1)
    :return:
    9%
    """
    n, k = [int(x) for x in input().split(" ")]
    number = input().split(" ")
    if len(number) > n:
        raise Exception("Index Out of Range.")
    else:
        number = [int(x) for x in number]
    pairs = []
    for i in number:
        for j in number:
            pairs.append((i, j))
    print(sorted(pairs)[k-1])


def solution04():
    """
    题目描述：
n个数的伪中位数定义为从小到大排序后第⌊(n+1)/2⌋个数。其中，⌊x⌋的意思是x向下取整。

现在，给你n个数，你需要向其中增加最少的数，使得k成为最后这一组数的伪中位数。

请问你需要加入数的最少数。

输入
输入第一行包含两个数n,k,意为原来数的个数和最后的伪中位数。

接下来一行n个数a_i，空格隔开，代表原来的数。

1≤n≤500,1≤a_i≤100000

输出
输出一个数，你需要加入数的最少数量。


样例输入
4 2
2 3 3 3
样例输出
2

提示
样例解释：加入1,1后,原数组变为1,1,2,3,3,3,其伪中位数为2。
    :return:
    18%
    """
    n, k = [int(x) for x in input().split(" ")]
    number = input().split(" ")
    if len(number) > n:
        raise Exception("Index Out of Range.")
    else:
        number = sorted([int(x) for x in number])
        now_mid_idx = (n+1) >> 1
        now_mid = number[now_mid_idx]
        if now_mid == k:
            print(0)
        else:
            print(now_mid_idx - number.index(k))



def solution05():
    """
    题目描述：
现在有两个串S和T，你需要从S中取出一个子串，并且从T中取出一个子序列，使得两个取出来的串一样。

这样不同的方案有多少？答案对10^9+7取模。

子串的意思是在字符串中截取连续一段，比如bc是abcd的子串。

子序列的意思是在字符串中截取不一定连续的几段（也可以是一段）连在一起，比如ac是abcd的子序列。

注意，在本题中，两种取法位置不同，但是取出来的字符串是相同的情况算作两种不同的情况，详见样例解释。

输入
输入包含两个字符串S,T  一行一个字符串

|S|,|T|≤5000

输出
输出包含一个数，代表答案对10^9+7取模。


样例输入
aaa
aaa
样例输出
16

提示
样例解释
S有6个子串，T有7个子序列。
S的6个子串：a(1),a(2),a(3),aa(12),aa(23),aaa(123);
T的7个子序列：a(1),a(2),a(3),aa(12),aa(23),aa(13),aaa(123);
可以得知，如果这个相同的串为a，有3×3种取法，如果这个相同的串为aa，有2×3种取法，如果这个相同的串为aaa，有1×1种取法。
总共有16种取法。
    :return:
    53%
    """
    # S = input()
    # T = input()
    S = "aaa"
    T = "aaa"
    if not S or not T:
        print(0)
        return
    s_substr_list = []
    for i in range(len(S)):
        for j in range(len(S) - i):
            s_substr_list.append(S[j: i + j + 1])
    def sub(arr):
        finish = []  # the list containing all the subsequences of the specified sequence
        size = len(arr)  # the number of elements in the specified sequence
        end = 1 << size  # end=2**size
        for index in range(end):
            array = []  # remember to clear the list before each loop
            for j in range(size):
                if (index >> j) % 2:  # this result is 1, so do not have to write ==
                    array.append(arr[j])
            finish.append(array)
        return finish
    t_series_list = ["".join(x) for x in sub(T) if x]
    result = 0
    for s in s_substr_list:
        result += t_series_list.count(s)
    print(result)




if __name__ == '__main__':
    # solution01()
    # solution02()
    # solution03()
    # solution04()
    solution05()



