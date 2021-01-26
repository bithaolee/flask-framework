from flask import g
from werkzeug.local import LocalProxy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .config import config


db_cfg = config('db')

engine = create_engine(
    f'mysql+pymysql:///{db_cfg["user"]}:{db_cfg["password"]}@{db_cfg["host"]}:{db_cfg["port"]}/{db_cfg["database"]}',
    convert_unicode=True,
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收(重置)
)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = db_session()
    return db

db = LocalProxy(get_db)