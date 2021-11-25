import json
from flask import request, Blueprint
from flask_restplus import Api, Resource, fields, Namespace

from Python_Applications.python_web.flask_app.utils.result import success, error
from Python_Applications.python_web.flask_app.utils.mysql_interface import MysqlInterface
mi = MysqlInterface()
common_blueprint = Blueprint("common", __name__)
common_api = Api(common_blueprint, title="公用统一接口", description="包含保存、查询（详情、列表）、删除、修改等接口")

common_ns = Namespace("common", description="统一接口模块")

model = common_ns.model('CommonModel', {
    'module_name': fields.String(required=True, description='模块名称'),
    'params_json': fields.String(required=True, description='json数据'),
})


@common_ns.route("/<int:obj_id>", doc={'description': '详情、删除、修改接口'})
class QueryOrUpdateData(Resource):
    @common_ns.expect()
    def get(self, obj_id):
        obj_result = mi.query(f"select * from table_data where id = {obj_id}")['fetch']
        if len(obj_result) > 0:
            return success(obj_result[0]['params_json'])
        else:
            return error('数据查询失败')

    @common_ns.expect(model)
    def put(self, obj_id):
        params_json = request.get_json()['params_json']
        print(params_json)
        update_result = mi.query(f"update table_data set params_json = '{params_json}' where id = {obj_id}")
        if update_result:
            return success()
        else:
            return error('更新失败')

    @common_ns.expect()
    def delete(self, obj_id):
        update_result = mi.query(f"delete from table_data where id = {obj_id}")
        if update_result:
            return success()
        else:
            return error('删除失败')


@common_ns.route("/data", doc={'description': '保存、列表查询接口'})
class QueryOrSaveData(Resource):
    @common_ns.expect()
    def post(self):
        json_data = request.get_json()
        print(json_data)
        module_name = json_data['module_name']
        params_json = json_data['params_json']
        save_result = mi.query(
            f"""insert into table_data (name, params_json) values ('{module_name}', '{params_json}')""")
        if save_result:
            return success()
        else:
            return error('保存失败')

    @common_ns.expect()
    def get(self):
        args_data = request.args
        print(args_data)
        rows = mi.query(f"""select * from table_data where name = '{args_data['module_name']}' order by id desc""")['fetch']
        result_list = []
        filter_list = []
        is_filter = False
        for row in rows:
            tmp_dict = json.loads(row["params_json"])
            tmp_dict['module_name'] = row['name']
            tmp_dict['id'] = row['id']
            for key in args_data.keys():
                if key != 'module_name' and args_data[key]:
                    is_filter = True
                    if str(tmp_dict[key]).__contains__(args_data[key]):
                        filter_list.append(tmp_dict)
            result_list.append(tmp_dict)
        result_list = filter_list if is_filter else result_list
        return success(result_list[:10])
