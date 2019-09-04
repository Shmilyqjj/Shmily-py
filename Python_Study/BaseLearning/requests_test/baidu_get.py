#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: get baidu / search baidu
:Owner: jiajing_qu
"""

import requests

#访问
# response = requests.get('https://www.baidu.com')
# print(response.status_code)
# print(response.encoding)
# print(response.apparent_encoding)
# response.encoding = 'utf-8'
# print(response.text)
# print('访问百度成功，接下来搜索')


#搜索
# wd = input('输入要搜索的内容:')
# res = requests.get('http://www.baidu.com/s?wd=%s' % wd)
# if res.status_code == 200:
#     res.encoding = 'utf-8'
#     print(res.text)


#方法
url = 'http://www.baidu.com/s?'
# res = requests.get(url)
# print( requests.head(url) ) #获得网页头信息
# print( res.headers )        #获得header内容

#requests可以使用任何方法
# req = requests.request('get',url)
# req.encoding = 'utf-8'
# print(req.text)

host = 'http://httpbin.org/'
res = requests.request('post',host)
print(res.text)




