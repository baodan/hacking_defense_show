from flask import make_response
import json
from tools.json_update import CJsonEncoder


def return_data(message, status_code=200, headers=None, json_update=False):
    # 定制返回格式
    data_format = {
        'status': status_code,
        'data': message
    }
    # 添加json对日期、有小数点数值的处理
    if json_update:
        data = json.dumps(data_format, cls=CJsonEncoder)
    else:
        data = json.dumps(data_format)
    if headers:
        headers['Content-Type'] = 'application/json'
        return make_response(data, status_code, headers=headers)
    else:
        return make_response(data, status_code, {'Content-Type': 'application/json'})