import time
import uuid


def make_response_dict(status, msg, body):
    resp = {
        "status": status,
        "msg": msg,
        "body": body
    }

    return resp


def get_time(sec=None):
    """sec 为空时返回当前系统时间，否则返回指定秒数对应的时间"""
    if not sec:
        lt = time.localtime()
    else:
        lt = time.localtime(sec)

    now = '%s-%02d-%02d %02d:%02d:%02d' % (lt[0], lt[1], lt[2], lt[3], lt[4],
                                           lt[5])

    return now


def get_time_sec():
    return time.time()


def generate_uuid():
    return str(uuid.uuid4())


def expire(datetime):
    now = get_time()
    time_fmt = '%Y-%m-%d %H:%M:%S'
    if time.strptime(now, time_fmt) > time.strptime(datetime, time_fmt):
        return True
    else:
        return False
