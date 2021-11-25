from flask import request, Blueprint
from flask_restplus import Api, Resource, fields, Namespace

from Python_Applications.python_web.flask_app.utils.result import success, error
from Python_Applications.python_web.flask_app.utils.mysql_interface import MysqlInterface
mi = MysqlInterface()
financial_blueprint = Blueprint("financial", __name__)
financial_api = Api(financial_blueprint, title="融资门户", description="融资门户模块API")

financial_ns = Namespace("financial-portal", description="融资门户模块")

model = financial_ns.model('FinancialModel', {
    'params_json': fields.String(required=True, description='json数据'),
})

@financial_ns.route("/enterprise-certification", doc={'description': '企业认证(四步)'})
class SaveEnterprise(Resource):
    @financial_ns.expect(model)
    def post(self):
        print(request.get_json())
        params_json = request.get_json()['params_json']
        mi.query(f"insert into table_data (name, params_json) values ('enterprise', '{params_json}')")
        return request.get_json()

