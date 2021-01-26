import redis as _redis
from flask import current_app
from werkzeug.local import LocalProxy

host = current_app.config.get('REDIS_HOST')
port = current_app.config.get('REDIS_PORT')
db = current_app.config.get('REDIS_DB')

pool = _redis.ConnectionPool(host=host, port=port, db=db, decode_responses=True)


def get_conn():
    return _redis.StrictRedis(connection_pool=pool)


redis = LocalProxy(get_conn)