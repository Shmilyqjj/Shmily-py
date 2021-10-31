#!/usr/bin/env python
# encoding: utf-8
"""
:Description:文件上传下载
:Author: shmily
:Create Time: 2021/10/30 下午8:17
:@File: file_utils.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""
import time
from flask_restplus import Namespace, Resource, fields
from flask import request, Blueprint, send_from_directory
from Python_Applications.python_web.flask_app.conf.config import config
import os
from Python_Applications.python_web.flask_app.utils.result import *

basedir = os.path.abspath(os.path.dirname(__file__))
file_blueprint = Blueprint("file-api", __name__)
file_ns = Namespace("file-api", description="文件管理模块")
file_model = file_ns.model('FileModel', {'file': fields.String(readOnly=True, description='文件')})


@file_ns.route("/upload", doc={'description': '文件上传到服务器'})
class UploadFile(Resource):
    @file_ns.expect(file_model)
    def post(self):
        file = request.files.get('file')
        file_dir = os.path.join(basedir.replace('functions', ''), config.get("db").UPLOAD_FOLDER)
        file_name = file.filename + "_" + str(time.time())
        print(file_name)
        try:
            file.save(os.path.join(file_dir, file_name))
            return success(file_name)  # http://192.168.xx.xxx:5000/files/tips_1635646256.1896794
        except Exception as e:
            return error(f"文件上传失败请重新上传{e}")


@file_ns.route("/download/<path:path>", doc={'description': '文件上传到服务器'})
class DownloadFile(Resource):
    @file_ns.expect(file_model)
    def get(self, path):
        try:
            if os.path.isdir(path):
                return error("Download error.Wrong path name.")
            else:
                name = path.split('\\')[-1]
                file_path = "static/"
                return send_from_directory(file_path, name, as_attachment=True)
        except:
            return error("文件不存在或无法下载")
