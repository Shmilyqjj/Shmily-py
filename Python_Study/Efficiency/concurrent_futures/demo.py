#!/usr/bin/env python
# encoding: utf-8
"""
:Description:concurrent.futures demo代码
:Author: 佳境Shmily
:Create Time: 2020/7/26 22:26
:File: demo
:Site: shmily-qjj.top
"""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests


def load_url(url):
    return requests.get(url)


url = 'http://httpbin.org'
executor = ThreadPoolExecutor(max_workers=1)
future = executor.submit(load_url, url)
print(future.done())
print(future.result().status_code)