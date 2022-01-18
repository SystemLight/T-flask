def make_error(msg="error", code=400, data=None):
    return {"code": code, "msg": msg, "data": data}


def make_unauthorized(msg="error", code=401, data=None):
    return make_error(msg, code, data)


def make_ok(msg="ok", code=200, data=None):
    return {"code": code, "msg": msg, "data": data}
