import math
import decimal
from typing import Union, List, Set

from sqlalchemy import text

from .model import BaseMixin
from ..core.db import db


Orders = List[Set(str, Union(str, int, decimal.Decimal))]


class BaseMgr:

    def get_page(self, cls_:BaseMixin, filters:set, orders:Orders=list(), field:tuple=(), page:int=1, per_page:int=10)->dict:
        '''获取分页数据
        @param BaseMixin cls 数据库模型实体类
        @param set filters 查询条件
        @param str order 排序
        @param tuple field 返回字段
        @param int page 页码
        @param int per_page 每页数据数量
        @return dict
        '''
        res = {
            'page': {
                'current_page': page,
                'per_page': per_page,
                'total_page': 0,
                'count': 0,
            },
            'items': []
        }
        query = db.query(cls_).filter(*filters)
        
        if hasattr(cls_, 'deleted_at'):
            query = query.filter(cls_.deleted_at==0)

        res['page']['count'] = query.count()
        res['page']['total_page'] = math.ceil(res['page']['count'] / per_page)

        for order in orders:
            field, sort = order
            sort = 'desc' if sort not in ['asc', 'desc'] else sort
            query = query.order_by(text(f'{field} {sort}'))

        data = query.offset((page-1)*per_page).limit(per_page)
        if not field:
            res['items'] = [item.to_dict() for item in data]
        else:
            res['items'] = [item.to_dict(only=field) for item in data]
        
        return res


    def get_first(self, cls_:BaseMixin, filters:set, orders:Orders=list(), field: tuple=())->dict:
        query = db.query(cls_).filter(*filters)

        if hasattr(cls_, 'deleted_at'):
            query = query.filter(cls_.deleted_at==0)

        for order in orders:
            field, sort = order
            sort = 'desc' if sort not in ['asc', 'desc'] else sort
            query = query.order_by(text(f'{field} {sort}'))

        item = query.first()
        return item.to_dict() if item is not None else {}


    def add(self, cls_:BaseMixin, data:dict)->int:
        item = cls_(**data)
        db.add(item)
        db.flush()
        return item.id


    def update(self, cls_:BaseMixin, data:dict, filters:set)->bool:
        pass


    def delete(self, cls_:BaseMixin, filters:set)->int:
        query = db.query(cls_).filter(*filters)

        if hasattr(cls_, 'deleted_at'):
            query = query.filter(cls_.deleted_at==0)

        id = 0
        item = query.first()
        if item is not None:
            id = 1
            if hasattr(item, 'delete'):
                item.delete()
            else:
                db.delete(item)
        db.commit()
        return id


    def count(self, cls_:BaseMixin, filters:set, filed=None)->int:
        pass