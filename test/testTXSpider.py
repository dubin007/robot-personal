import unittest
from src.spider.TXSpider import TXSpider
import re

from src.util.constant import AREA_TAIL


class testNcovWeRobot(unittest.TestCase):

    def setUp(self) -> None:
        self.sp = TXSpider()

    def test_get_info(self):
        data = self.sp.get_raw_real_time_info()
        assert len(data) > 0

    def test_parse_info(self):
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

        last = self.sp.change_raw_data_format(data1)
        now = self.sp.change_raw_data_format(data2)
        update_city = self.sp.parse_increase_info(now, last)
        assert len(update_city) == 3
        assert update_city[0]['city'] == '武汉'
        assert update_city[1]['area'] == '加拿大'
        assert update_city[2]['area'] == '湖北'


    def test_get_state_all(self):
        state_dict = self.sp.get_state_all()
        print(state_dict)

    def test_get_short_name(self):
        area1 = '重庆市'
        area2 = '重庆'
        area3 = '某某自治区'
        area4 = '杭州'
        assert re.subn(AREA_TAIL, '', area1)[0] == '重庆'
        assert re.subn(AREA_TAIL, '', area2)[0] == '重庆'
        assert re.subn(AREA_TAIL, '', area3)[0] == '某某'
        assert re.subn(AREA_TAIL, '', area4)[0] == '杭州'

    def test_fill_unknown(self):
        data = [{'confirm': 2823, 'dead': 81, 'heal': 55, 'suspect': 5794, 'country': '中国'}]
        res = [{'confirm': 2823, 'dead': 81, 'heal': 55, 'suspect': 5794, 'area': '中国', 'country': '中国', 'city': '中国'}]
        assert res == self.sp.fill_unknow(data)

    def test_main(self):
        self.sp.main()
