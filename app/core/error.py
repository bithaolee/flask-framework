from enum import IntEnum

from flask import jsonify
from werkzeug.exceptions import HTTPException


class Code(IntEnum):
    OK = 0
    UNAHTHORIZED = 10000
    INVALID_INPUT = 20000
    NOT_FOUND = 30000
    HTTP_ERROR = 40000
    SERVER_ERROR = 50000 # 服务器内部错误
    UNKNOW = 99999 # 未知错误


class AppException(Exception):

    msg = '服务器繁忙，请稍后再试~'

    data = None

    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        self.data = data

    def __str__(self):
        return self.msg


def handle_error(e):
    data = []
    if isinstance(e, HTTPException):
        code = Code.HTTP_ERROR.value
        msg = str(e)
    elif isinstance(e, AppException):
        code = e.code
        msg = e.msg
        data = e.data if e.data else []
    else:
        code = Code.UNKNOW.value
        msg = '未知错误，请稍后再试~'
        # 记录日志
        print(e)
        raise e

    return jsonify(dict(code=code, msg=msg, data=data))