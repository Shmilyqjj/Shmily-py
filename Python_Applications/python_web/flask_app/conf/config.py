#!/usr/bin/env python
# encoding: utf-8
"""
:Author: shmily
:Create Time: 2021/10/30 上午10:46
:@File: config.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__)).replace("conf", "")


class Config:
    UPLOAD_FOLDER = "static"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DBConfig(Config):
    DATABASE_IP = os.environ.get('DATABASE_IP') or "192.168.2.21"
    DATABASE_PORT = os.environ.get('DATABASE_PORT') or "3306"
    DATABASE_USER = os.environ.get('DATABASE_USER') or "root"
    DATABASE_PWD = os.environ.get('DATABASE_PWD') or "Smy12345"
    DATABASE_NAME = os.environ.get('DATABASE_NAME') or "wangwangdb"


config = {
    'app': Config,
    'db': DBConfig,
}
