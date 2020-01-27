import unittest

import itchat

from src.robot.NcovWeRobotFunc import *
from src.robot.NcovWeRobotServer import do_ncov_update
from src.spider.TXSpider import TXSpider
from src.util.constant import SHOULD_UPDATE, UPDATE_CITY, UN_REGIST_PATTERN2
from src.util.redis_config import connect_redis, save_json_info, save_json_info_as_key
import jieba

class testNcovWeRobot(unittest.TestCase):

    def setUp(self) -> None:
        self.sp = TXSpider()

    def testCheckRegister(self):
        assert check_whether_register("订阅湖北") == True
        assert check_whether_register("不订阅") == False
        assert check_whether_register("订阅") == False

    def testCheckUnregist(self):
        assert check_whether_unregist("取消湖北") == True
        assert check_whether_unregist("取消") == False
        assert check_whether_unregist("取关湖北") == True
        assert re.subn(UN_REGIST_PATTERN2, "", "取消湖北")[0] == '湖北'
        assert re.subn(UN_REGIST_PATTERN2, "", "取消关注湖北")[0] == '湖北'
        assert re.subn(UN_REGIST_PATTERN2, "", "取关湖北")[0] == '湖北'

    def test_user_subscribe(self):
        conn = connect_redis()
        succ, failed = user_subscribe(conn, 'test', '订阅湖北', jieba)
        assert succ == ['湖北']

    def test_do_ncov_update(self):
        data1 = [{"country": "中国", "area": "湖北", "city": "武汉", "confirm": 618, "suspect": 0, "dead": 45, "heal": 40},
                {"country": "中国", "area": "湖北", "city": "黄冈", "confirm": 122, "suspect": 0, "dead": 2, "heal": 2},
                {"country": "中国", "area": "湖北", "city": "孝感", "confirm": 55, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "荆门", "confirm": 38, "suspect": 0, "dead": 1, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "恩施州", "confirm": 17, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "荆州", "confirm": 33, "suspect": 0, "dead": 2, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "仙桃", "confirm": 11, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "十堰", "confirm": 20, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "随州", "confirm": 36, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "天门", "confirm": 5, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "宜昌", "confirm": 20, "suspect": 0, "dead": 1, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "鄂州", "confirm": 1, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "咸宁", "confirm": 43, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "广东", "city": "广州", "confirm": 17, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "加拿大", "area": "", "city": "", "confirm": 1, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "法国", "area": "", "city": "", "confirm": 3, "suspect": 0, "dead": 0, "heal": 0}]

        data2 = [{"country": "中国", "area": "湖北", "city": "武汉", "confirm": 698, "suspect": 0, "dead": 45, "heal": 40},
                {"country": "中国", "area": "湖北", "city": "黄冈", "confirm": 122, "suspect": 0, "dead": 2, "heal": 2},
                {"country": "中国", "area": "湖北", "city": "孝感", "confirm": 55, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "荆门", "confirm": 38, "suspect": 0, "dead": 1, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "恩施州", "confirm": 17, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "荆州", "confirm": 33, "suspect": 0, "dead": 2, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "仙桃", "confirm": 11, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "十堰", "confirm": 20, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "随州", "confirm": 36, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "天门", "confirm": 5, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "宜昌", "confirm": 20, "suspect": 0, "dead": 1, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "鄂州", "confirm": 1, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "湖北", "city": "咸宁", "confirm": 43, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "中国", "area": "广东", "city": "广州", "confirm": 17, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "加拿大", "area": "", "city": "", "confirm": 2, "suspect": 0, "dead": 0, "heal": 0},
                {"country": "法国", "area": "", "city": "", "confirm": 3, "suspect": 0, "dead": 0, "heal": 0}]
        # 完成数据转化并更新数据库
        last = self.sp.change_raw_data_format(data1)
        now = self.sp.change_raw_data_format(data2)
        update_city = self.sp.parse_increase_info(now, last)
        self.sp.re.set(SHOULD_UPDATE, 1)
        save_json_info_as_key(self.sp.re, UPDATE_CITY, update_city)
        itchat.auto_login()
        user_subscribe(self.sp.re, 'filehelper', '订阅湖北重庆', jieba)
        do_ncov_update(self.sp.re, itchat)