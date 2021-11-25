from flask import request, Blueprint
from flask_restplus import Api, Resource, fields, Namespace

from Python_Applications.python_web.flask_app.utils.result import success, error

user_blueprint = Blueprint("user", __name__)
user_api = Api(user_blueprint, title="用户管理", description="用户管理模块API")

ns = Namespace("user-api", description="用户管理模块")

user_model = ns.model('UserModel', {
    'user_id': fields.String(readOnly=True, description='用户ID'),
    'username': fields.String(required=True, description='用户名称'),
})


@ns.route("/user/<int:user_id>", doc={'description': '查询单个用户，传入用户ID'})
class getUserApi(Resource):
    @ns.expect()
    def get(self, user_id):
        return error()


@ns.route("/user", doc={'description': '保存用户'})
class getUserList(Resource):
    @ns.expect(user_model)
    def post(self):
        print(request.get_json())
        print(request.get_data())
        return request.get_json()
