#!/usr/bin/env python
# encoding: utf-8
"""
测试session cookie
:Author: shmily
:Create Time: 2021/10/30 下午2:44
:@File: session.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""

from flask import Flask, url_for, request, render_template, redirect, session
app = Flask('hello_flask')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("user") == 'admin':
            session['user'] = request.form['user']
            return 'Admin login successfully!'
        else:
            return 'No such user!'
    if 'user' in session:
        return 'Hello %s!' % session['user']
    else:
        title = request.args.get('title', 'Default')
        return "hello flask %s" % title


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


app.secret_key = '123456'
if __name__ == "__main__":
    app.run(debug=True)
