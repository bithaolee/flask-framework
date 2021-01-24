from enum import EnumInt

from flask import jsonify


class Error(EnumInt):
    UNAHTHORIZED = 10000
    UNKNOW = 50000


class AppException(Exception):

    def __init(self, code, msg):
        pass

    def __repr__(self):
        pass


def register_error_handler(app):
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        return jsonify(dict(code=Error.UNKNOW, msg='服务器繁忙，请稍后再试~'))