import unittest
from src.robot.NcovWeRobotFunc import *

class testNcovWeRobot(unittest.TestCase):

    def testCheckRegister(self):
        assert check_whether_register("订阅湖北") == True
        assert check_whether_register("不订阅") == False
        assert check_whether_register("订阅") == False