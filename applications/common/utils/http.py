from flask import jsonify


def success_api(msg: str = "成功", data=None):
    """ 成功响应 默认值 成功 """
    return jsonify(code=200, msg=msg, data=data)


def fail_api(msg: str = "失败", data=None):
    """ 失败响应 默认值 失败 """
    return jsonify(code=400, msg=msg, data=data)
