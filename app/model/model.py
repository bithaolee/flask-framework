import time
import datetime
import decimal

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime,
    UniqueConstraint, Index
)


Base = declarative_base()


class SoftDeleteMixin:
    '''软删除，需要执行软删除的表继承此类'''

    deleted_at = Column(Integer, nullable=True, default=0)

    def delete(self):
        self.deleted_at = int(time.time())


class BaseMixin(Base):

    __abstract__ = True

    """model的基类,所有model都必须继承"""
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, 
                        onupdate=datetime.datetime.now, index=True)

    def to_dict(self, only=None):
        '''将数据对象转换为dict格式
        :param None or set only 保留的字段
        '''
        ret_dict = {}
        for item in self.__table__.columns:
            key = item.name
            if only is not None and key not in only:
                continue
            value = getattr(self, key)
            if isinstance(value, decimal.Decimal):
                ret_dict[key] = float(value)
            elif isinstance(value, datetime.datetime):
                ret_dict[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, datetime.date):
                ret_dict[key] = value.strftime('%Y-%m-%d')
            else:
                ret_dict[key] = value
        return ret_dict


class User(BaseMixin):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(128), nullable=False)