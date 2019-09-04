#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 系统库itertools
:Owner: jiajing_qu
"""
import itertools

#无限迭代器 无限输出自然数
# naturals = itertools.count(1)
# for n in naturals:
#     print(n)


#无限迭代器 无限按顺序输出
# l=[7,1,0,5,5,2,9,0,7]
# cs = itertools.cycle(l)
# for s in cs:
#     print(s)

#可以限定重复次数
# ns = itertools.repeat('zz',5)
# for n in ns:
#     print(n)

'''无限序列只有在for迭代时才会无限地迭代下去，如果只是创建了一个迭代对象，
它不会事先把无限个元素生成出来，事实上也不可能在内存中创建无限多个元素。'''

#takewhile()等函数根据条件判断来截取出一个有限的序列
# naturals = itertools.count(1)
# naturals = itertools.takewhile(lambda x:x<=10,naturals)
# for n in naturals:
#     print(n)

#groupby()把迭代器中相邻的重复元素挑出来放在一起：
l=[7,1,0,5,5,2,9,0,7]
for key,group in itertools.groupby(l):
    print(key,list(group))

#全排列
l = [1,2,3]
s = itertools.permutations(l)
print(list(s))

