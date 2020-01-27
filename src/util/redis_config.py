import redis
from src.util.constant import REDIS_HOST


def connect_redis():
    pool = get_pool()
    conn = redis.Redis(connection_pool=pool)
    return conn

def get_pool():
    pool = redis.ConnectionPool(host=REDIS_HOST, port=6379, decode_responses=True)
    return pool