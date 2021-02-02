import math
import decimal
from typing import Union, List, Set

from sqlalchemy import text

from .model import BaseMixin
from ..core.db import db


Orders = List[Set(str, Union(str, int, decimal.Decimal))]


class BaseManager:

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


    def get_all(self, cls_:BaseMixin, filters:set, orders:Orders=list(), field:tuple=(), limit:int=0)->list:
        '''获取所有满足条件的数据
        @param BaseMixin cls 数据库模型实体类
        @param set filters 查询条件
        @param str order 排序
        @param tuple field 返回字段
        @param int limit 取数据最大数量
        @return list
        '''
        query = db.query(cls_)
        
        if filters:
            query = query.filter(*filters)

        if hasattr(cls_, 'deleted_at'):
            query = query.filter(cls_.deleted_at==0)

        for order in orders:
            field, sort = order
            sort = 'desc' if sort not in ['asc', 'desc'] else sort
            query = query.order_by(text(f'{field} {sort}'))

        if limit != 0:
            query = query.limit(limit)
        
        query = query.all()

        if not field:
            items = [item.to_dict() for item in items]
        else:
            items = [item.to_dict(only=field) for item in items]
        
        return items


    def get_first(self, cls_:BaseMixin, filters:set, orders:Orders=list(), field:tuple=())->dict:
        '''获取所有满足条件的第一条数据
        @param BaseMixin cls 数据库模型实体类
        @param set filters 查询条件
        @param str order 排序
        @param tuple field 返回字段
        @return dict
        '''
        items = self.get_all(cls_, filters, orders, field, limit=1)
        return items[0] if items else None


    def add(self, cls_:BaseMixin, data:dict)->int:
        '''插入一条数据
        @param BaseMixin cls 数据库模型实体类
        @param dict data 数据
        @return int 插入数据的主键
        '''
        item = cls_(**data)
        db.add(item)
        db.flush()
        return item.id


    def update(self, cls_:BaseMixin, data:dict, filters:set)->int:
        '''更新数据
        @param BaseMixin cls 数据库模型实体类
        @param dict data 数据
        @param set filters 过滤条件
        @return int 影响的行数
        '''
        query = db.query(cls_).filter(*filters)

        if hasattr(cls_, 'deleted_at'):
            query = query.filter(cls_.deleted_at==0)

        return query.update(data, synchronize_session=False)


    def delete(self, cls_:BaseMixin, filters:set)->int:
        '''更新数据
        @param BaseMixin cls 数据库模型实体类
        @param set filters 过滤条件
        @return int 影响的行数
        '''
        query = db.query(cls_).filter(*filters)

        if hasattr(cls_, 'deleted_at'):
            items = query.filter(cls_.deleted_at==0).all()
            for item in items:
                item.delete()
            affect_rows = len(items)
        else:
            affect_rows = query.filter(*filters).delete(synchronize_session=False)
        db.commit()
        return affect_rows


    def count(self, cls_:BaseMixin, filters:set, field=None)->int:
        '''获取满足条件的总行数
        @param BaseMixin cls 数据库模型实体类
        @param set filters 过滤条件
        @param string|None field 统计的字段
        @return int
        '''
        query = db.query(cls_).filter(*filters)

        if hasattr(cls_, 'deleted_at'):
            query = query.filter(cls_.deleted_at==0)
        
        if field is None:
            return query.count()
        else:
            return query.count(field)
