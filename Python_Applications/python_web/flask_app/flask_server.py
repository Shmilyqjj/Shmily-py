from flask import Flask

import os
from flask_cors import CORS
from Python_Applications.python_web.flask_app.functions.file_utils import file_blueprint, file_ns

from flask_restplus import Api
from datetime import timedelta
from users.login import user_blueprint, user_ns
from common.router import common_blueprint, common_ns

#  图片访问 http://192.168.12.239:5000/files/imgtest.jpg
app = Flask(__name__, static_folder='static/', static_url_path='/files')
api = Api(app,
          version="1.0",
          title="新零售供应链金融平台",
          description="新零售供应链金融平台API")
api.add_namespace(user_ns)
api.add_namespace(file_ns)
api.add_namespace(common_ns)
app.register_blueprint(user_blueprint)
app.register_blueprint(file_blueprint)
app.register_blueprint(common_blueprint)
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=3600)  # Session超时时间

CORS(app, resources=r'/*')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
