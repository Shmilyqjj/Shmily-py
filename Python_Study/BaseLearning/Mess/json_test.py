#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: json库 常用方法
:Owner: jiajing_qu
"""
import json

example_json = {'a': '1111', 'c': '3333', 'b': '2222', 'd': '4444'}

# json.dumps()用于将dict类型的数据转成str
json_str = json.dumps(example_json)
print(json_str,type(json_str))

# json.loads()用于将str转dict
json_obj = json.loads(json_str)
print(json_obj,type(json_obj))

# json.dump()  将json存文件
fp = file('C:\Users\jiajing_qu\PycharmProjects\Shmily-py\Python_Study\BaseLearning\Mess\example_json.json', 'w')
print(type(fp))
json_object = json.dump(example_json,fp=fp)
fp.close()

# json.load() 从json文件中读取数据
fp = file('C:\Users\jiajing_qu\PycharmProjects\Shmily-py\Python_Study\BaseLearning\Mess\example_json.json', 'r')
dic = json.load(fp)
print(dic)