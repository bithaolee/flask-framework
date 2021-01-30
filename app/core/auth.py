from functools import wraps

from flask import g, request, jsonify

from .error import Code


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return jsonify(dict(code=Code.OK.value, msg='ok'))
        return f(*args, **kwargs)
    return wrapper