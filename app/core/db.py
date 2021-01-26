from flask import current_app, g
from werkzeug.local import LocalProxy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

host = current_app.config.get('DB_HOST')
port = current_app.config.get('DB_PORT')
user = current_app.config.get('DB_USER')
password = current_app.config.get('DB_PASSWORD')
database = current_app.config.get('DB_DATABASE')

engine = create_engine(
    f'mysql+pymysql:///{user}:{password}@{host}:{port}/{database}',
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

def close_db():
    db = g.pop('_database', None)
    if db is not None:
        db.close()

db = LocalProxy(get_db)