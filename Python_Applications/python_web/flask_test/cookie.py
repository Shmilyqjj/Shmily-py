#!/usr/bin/env python
# encoding: utf-8
"""
:Author: shmily
:Create Time: 2021/10/30 下午3:03
:@File: cookie.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""
from flask import Flask,url_for,request,render_template,redirect,session,make_response
import time
app = Flask("hello_flask")

# curl -s -XPOST -H "Content-Type: application/json" "http://127.0.0.1:5000/login" -d '{"user":"admin"}'


@app.route('/login', methods=['POST', 'GET'])
def login():
    response = None
    if request.method == 'POST':
        print(request.get_json())
        if request.get_json()['user'] == 'admin':
            session['user'] = request.get_json()['user']
            response = make_response('Admin login successfully!')
            response.set_cookie('login_time', time.strftime('%Y-%m-%d %H:%M:%S'))
    # curl -s -XGET "http://127.0.0.1:5000/login"
    else:
        if 'user' in session:
            login_time = request.cookies.get('login_time')
            response = make_response('Hello %s, you logged in on %s' % (session['user'], login_time))

    return response


app.secret_key = '123456'
if __name__ == "__main__":
    app.run(debug=True)
