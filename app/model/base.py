import decimal
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime,
    UniqueConstraint, Index
)


Base = declarative_base()


class BaseMixin(Base):

    __abstract__ = True

    """model的基类,所有model都必须继承"""
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, 
                        onupdate=datetime.datetime.now, index=True)

    def as_dict(self):
        ret_dict = {}
        for item in self.__table__.columns:
            key = item.name
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