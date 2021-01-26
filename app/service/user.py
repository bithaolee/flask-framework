from ..core.redis import redis


class UserService:

    def get_user_by_token(self, token):
        user = redis.hgetall(f'session:{token}')
        return user

    def save_token(self, token, user):
        key = f'session:{token}'
        redis.hmset(key, user)
        redis.expire(key, 7*86400)