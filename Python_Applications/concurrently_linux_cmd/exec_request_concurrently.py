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


def exec_request(url, json, headers={'Content-Type':'application/json'}):
    res = requests.post(url, json=json, headers=headers)
    if res.status_code == 200:
        print('[success] ' + res.text)
    else:
        print('[failed] ' + res.text)


if __name__ == '__main__':
    concurrency = 20

    threads = []
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    for i in range(concurrency):
        if i % 2 == 0:
            thread = threading.Thread(target=exec_request, args=('https://url:port/v1/column/upsert', {"fqn": "xxx","comment": "人为改的","description": "我是艾迪啊，哈哈哈"}, header))
            threads.append(thread)
        else:
            thread = threading.Thread(target=exec_request, args=('https://url:port/v1/metadata/upsert', {"fqn": "xxx","operation":"ALTER_TABLE","operationTime":1690959107691,"columns":[{"name":"id","dataType":"int","comment":"listener的艾迪"},{"name":"name","dataType":"string","comment":"listener的"}],"ownerName":"hdfs","ownerType":"USER","createTime":1690958962000,"lastAccessTime":1690959107000}, header))
            threads.append(thread)

    for t in threads:
        t.start()
    for t in threads:
        t.join()





