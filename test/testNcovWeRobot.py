import unittest
from src.robot.NcovWeRobotFunc import *
from src.util.redis_config import connect_redis


class testNcovWeRobot(unittest.TestCase):

    def testCheckRegister(self):
        assert check_whether_register("订阅湖北") == True
        assert check_whether_register("不订阅") == False
        assert check_whether_register("订阅") == False

    def test_user_subscribe(self):
        conn = connect_redis()
        succ, failed = user_subscribe(conn, 'test', '订阅湖北')
        assert succ == ['湖北']