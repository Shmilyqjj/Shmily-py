#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 登入登出
:Author: shmily
:Create Time: 2021/10/30 下午4:05
:@File: login.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""
from flask import request, Blueprint, session
from flask_restplus import Resource, fields, Namespace
from Python_Applications.python_web.flask_app.utils.result import *
from Python_Applications.python_web.flask_app.utils.mysql_interface import MysqlInterface

mi = MysqlInterface()


user_blueprint = Blueprint("user-api", __name__)
# user_api = Api(user_blueprint, title="用户管理", description="用户管理模块API")
user_ns = Namespace("user-api", description="用户管理模块")
user_model = user_ns.model('UserModel', {
    'username': fields.String(readOnly=True, description='用户名'),
    'password': fields.String(required=True, description='密码'),
})
user_logout_model = user_ns.model('UserModel', {
    'username': fields.String(readOnly=True, description='用户名')
})


@user_ns.route("/user/login", doc={'description': '查询单个用户，传入用户ID'})
class LoginAPI(Resource):
    @user_ns.expect(user_model)
    def post(self):
        j = request.get_json()
        user = j.get('username')
        passwd = j.get('password')
        d = mi.query("select user_name,password from users").get('fetch')[0]
        if user == d.get("user_name") and passwd == d.get("password"):
            session['username'] = user
            return success('{"result": "user %s login successfully."}' % user)
        else:
            return error("用户或密码错误")


@user_ns.route("/user/logout", doc={'description': '查询单个用户，传入用户ID'})
class Logout(Resource):
    @user_ns.expect(user_logout_model)
    def post(self):
        j = request.get_json()
        if not j:
            return "data is null"
        user = j.get('username')
        print(session.get('username'))
        session.pop('username', user)
        return success('Logout successfully.')


