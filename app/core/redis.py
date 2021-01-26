import redis as _redis
from flask import current_app
from werkzeug.local import LocalProxy

from .config import config


redis_cfg = config('redis')

pool = _redis.ConnectionPool(host=redis_cfg['host'], port=redis_cfg['port'], db=redis_cfg['db'], decode_responses=True)


def get_conn():
    return _redis.StrictRedis(connection_pool=pool)


redis = LocalProxy(get_conn)