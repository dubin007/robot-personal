import unittest
from src.spider.TXSpider import TXSpider

class testNcovWeRobot(unittest.TestCase):

    def test_login(self):
        sp = TXSpider()
        sp.get_real_time_info()