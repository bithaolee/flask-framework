from sqlalchemy import Column, String, Integer

from .base import BaseMixin


class User(BaseMixin):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)