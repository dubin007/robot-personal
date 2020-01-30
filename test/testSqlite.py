import unittest

from src.util.constant import BASE_DIR
from src.util.sqlite_config import SQLiteConnect


class TestSqlite(unittest.TestCase):

    def setUp(self) -> None:
        self.sqlc = SQLiteConnect(BASE_DIR + "sqlite.db")

    def test_init_sqlite(self):
        pass

    def test_subscription(self):
        user = 'test1'
        city = '重庆'
        res = self.sqlc.query_subscription(user, city)
        self.sqlc.save_subscription(user, city)
        self.sqlc.save_subscription(user, city)
        res = self.sqlc.query_subscription(user, city)
        print(res)
        res = self.sqlc.cancel_subscription(user, city)
        assert res == 2

    def test_update_flag(self):
        flag = self.sqlc.get_update_flag()
        print(flag)
        self.sqlc.do_update_flag(1)
        res1 = self.sqlc.get_update_flag()
        assert res1 == 1
        self.sqlc.do_update_flag(flag)
