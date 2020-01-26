import unittest
from src.spider.TXSpider import TXSpider


class testNcovWeRobot(unittest.TestCase):

    def setUp(self) -> None:
        self.sp = TXSpider()

    def test_get_info(self):
        data = self.sp.get_raw_real_time_info()
        assert len(data) > 0

    def test_parse_info(self):
        data = [{"country": "中国", "area": "湖北", "city": "武汉", "confirm": 618, "suspect": 0, "dead": 45, "heal": 40},
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
        update_city = self.sp.parse_increase_info(data)
        print(update_city)

    def test_parse_info2(self):
        data = self.sp.get_raw_real_time_info()
        update_city = self.sp.parse_increase_info(data)
        print(update_city)
