#!/usr/bin/env python
# encoding: utf-8
"""
:Author: shmily
:@Desc: 并发请求接口 验证接口并发性
:@File: exec_cmd_concurrently_avg_time.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""
import threading
import requests


def exec_request():
    url = 'http://localhost:8080/api/stat/rt'
    headers = {
        'X-Real-IP': '101.28.185.115',
        'X-Forwarded-For': '101.28.185.115',
        'X-Real-Port': '6696',
        'Content-Type': 'application/octet-stream',
    }
    with open('/home/shmily/Projects/EnterpriseProjects/xunlei/GolangProjects/rcv_collector/test/rcv5_20111_data.bin',
              'rb') as binary_file:
        binary_data = binary_file.read()
    params = {
        'appId': '20111',
        'discardCount': '0',
        'sig': 'abcd',
        'callId': 'aaa',
        'octet': 'abcd'
    }

    res = requests.post(url, headers=headers, data=binary_data, params=params)

    if res.status_code == 200:
        print('[success] ' + res.text)
    else:
        print('[failed] ' + str(res.status_code) + " text:"  + res.text)


if __name__ == '__main__':
    concurrency = 3
    threads = []
    for i in range(concurrency):
        thread = threading.Thread(target=exec_request, args=[])
        threads.append(thread)
    for t in threads:
        t.start()
    for t in threads:
        t.join()





