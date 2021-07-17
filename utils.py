import datetime

STANDARD_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def now():
    return datetime.datetime.now().strftime(STANDARD_TIME_FORMAT)


def dt2str(dt: datetime.datetime):
    return dt.strftime(STANDARD_TIME_FORMAT)


def make_error(msg="error", code=400, data=None):
    return {"code": code, "msg": msg, "data": data}, code


def make_unauthorized(msg="error", code=401, data=None):
    return make_error(msg, code, data)


def make_ok(msg="ok", code=200, data=None):
    return {"code": code, "msg": msg, "data": data}, code
