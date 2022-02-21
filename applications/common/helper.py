from flask import abort, make_response, jsonify


def xss_escape(s: str):
    # xss过滤
    if s is None:
        return None
    else:
        return s.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;").replace("'", "&#39;").replace('"', "&#34;")


def validate(schema, data):
    errors = schema.validate(data)
    msg = ''
    for k, v in errors.items():
        for i in v:
            msg = "{}{}".format(k, i)
    if errors:
        abort(make_response(jsonify(code=400, msg=msg, data=None), 400))


def success(msg: str = "成功", data=None):
    return jsonify(code=200, msg=msg, data=data)


def fail(msg: str = "失败", data=None):
    return jsonify(code=400, msg=msg, data=data)
