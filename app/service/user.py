from ..model.user import User
from ..core.redis import redis
from ..core.db import db
from ..core.util import hash_password


class UserService:

    def get_user_by_token(self, token):
        user = redis.hgetall(f'session:{token}')
        return user


    def save_token(self, token, user):
        key = f'session:{token}'
        for field, value in user.items():
            redis.hset(key, field, value)
        redis.expire(key, 7*86400)
    

    def get_user_by_username(self, username):
        user = db.query(User).filter(User.username==username).first()
        return user.as_dict() if user else None
    

    def add_user(self, username, password):
        user = User(**dict(
            username=username,
            password=hash_password(password)
        ))
        db.add(user)
        db.commit()
        return user