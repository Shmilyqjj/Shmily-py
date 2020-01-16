#!/usr/bin/python3
# -*- coding,utf-8 -*-
"""
Description: dict 按key聚合成list
Author:曲佳境
Date: 2020/1/16 22,36
"""

# 方法1
from functools import reduce

# import pandas
# example = [["qjj","男"],["zxw","女"],["qjj","优秀"],["qjj","牛逼"],["qjj","棒棒"],["zxw","不优秀"],["zxw","不棒棒"],["cci","很强"],["cci","发展"],["cci","666"]]
# pandas_df = pandas.DataFrame(example, columns=['name','desc'])  # pandas接收一个list  转df
# # print(pandas_df)
# # 未完成


# 方法2
example = [{"qjj":"男"},{"zxw":"女"},{"qjj":"优秀"},{"qjj":"牛逼"},{"qjj":"棒棒"},{"zxw":"不优秀"},{"zxw":"不棒棒"},{"cci":"很强"},{"cci":"发展"},{"cci":"666"}]
result = {}
for dic in example:
    for k, v in dic.items():
        result.setdefault(k, []).append(v)
print(result)


