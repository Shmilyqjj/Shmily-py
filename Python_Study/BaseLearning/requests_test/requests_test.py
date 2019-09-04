#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: requests库 应用
:Owner: jiajing_qu
:Create time: 2019/8/28 20:25
"""
import requests


# res = requests.get('https://api.github.com/events')
# if res.status_code is 200:
#     print('get',res.text)
#
# # POST请求
# res = requests.post('http://httpbin.org/post', data = {'key-qjj':'value-zz'})
# print('post',res.text)
# print(res.content)
#
# # put
# res = requests.put('http://httpbin.org/put', data = {'key-qjj':'value-zz'})
# print('put',res.text)
# # delete
# res = requests.delete('http://httpbin.org/delete')
# print('delete',res.text)
# # head
# res = requests.head('http://httpbin.org/get')
# print('head',res.text)
# #options
# res = requests.options('http://httpbin.org/get')
# print('options',res.text)


cookie = requests.session().get('https://api.github.com/events').cookies
print(cookie)
print(cookie.get_dict())
# login的时候可以 data = {'username';'xx','password':'xx'}具体根据post请求的form表单的具体字段  然后data传给post（data=data），然后headers传递，然后cookies = cookie(这个cookie是cookie.get_dict()得到的，dict类型)


