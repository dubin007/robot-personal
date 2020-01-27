import redis
from src.util.constant import REDIS_HOST, STATE_NCOV_INFO
import json


def connect_redis():
    pool = get_pool()
    conn = redis.Redis(connection_pool=pool)
    return conn

def get_pool():
    pool = redis.ConnectionPool(host=REDIS_HOST, port=6379, decode_responses=True)
    return pool


def save_state_info(conn, data):
    conn.rpush(STATE_NCOV_INFO, json.dumps(data, ensure_ascii=False))


def load_last_info(conn):
    data_len = conn.llen(STATE_NCOV_INFO)
    if data_len == 0:
        return None
    elif data_len >= 10:
        conn.lpop(STATE_NCOV_INFO)
    last = json.loads(conn.lrange(STATE_NCOV_INFO, -1, -1)[0])
    return last
