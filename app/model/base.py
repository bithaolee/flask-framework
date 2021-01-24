from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index


Base = declarative_base()

class Model(Base):

    def as_dict(self):
        pass