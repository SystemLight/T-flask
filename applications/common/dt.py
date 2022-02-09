from datetime import datetime

STANDARD_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def now():
    return datetime.now().strftime(STANDARD_TIME_FORMAT)


def dt2str(dt: datetime):
    return dt.strftime(STANDARD_TIME_FORMAT)


def safe_strftime(dt: datetime):
    if isinstance(dt, datetime):
        return dt.strftime(STANDARD_TIME_FORMAT)
    return ""
