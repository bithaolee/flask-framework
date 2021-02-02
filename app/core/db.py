from functools import wraps

from flask import g
from werkzeug.local import LocalProxy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .config import config


_db_cfg = config('db')

engine = create_engine(
    f'mysql+pymysql://{_db_cfg["username"]}:{_db_cfg["password"]}@{_db_cfg["host"]}:{_db_cfg["port"]}/{_db_cfg["database"]}',
    echo=_db_cfg['echo'],
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收(重置)
)

_db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

def _get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = _db_session()
    return db


db = LocalProxy(_get_db)


def transaction(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # 用于测试，设置为False，不入库
        persist = kwargs.pop('persist', True)
        try:
            result = fn(*args, **kwargs)
        except Exception as e:
            db.rollback()
            raise e
        else:
            if persist:
                db.commit()
                return result
            else:
                db.rollback()
    return wrapper


def class_transaction(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        # 用于测试，设置为False，不入库
        persist = kwargs.pop('persist', True)
        try:
            result = fn(self, *args, **kwargs)
        except Exception as e:
            db.rollback()
            raise e
        else:
            if persist:
                db.commit()
                return result
            else:
                db.rollback()
    return wrapper