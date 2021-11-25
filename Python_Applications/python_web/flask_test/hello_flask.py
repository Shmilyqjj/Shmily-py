#!/usr/bin/env python
# encoding: utf-8
"""
:Author: shmily
:Create Time: 2021/10/22 下午5:27
:@File: hello_flask.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""

from flask import Flask
app = Flask('hello_flask')

@app.route('/')
def index():
    return "hello flask"


if __name__ == '__main__':
    app.debug = True
    app.run(port=8899)
