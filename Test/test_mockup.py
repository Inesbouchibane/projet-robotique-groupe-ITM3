import unittest
from unittest.mock import patch
from robot_mockup import RobotMockup

class TestRobotMockup(unittest.TestCase):
    
    def setUp(self):
        self.robot = RobotMockup("TestBot", 0, 0, 10, 20, 15, 5, "red")
    
    @patch("robot_mockup.uniform", return_value=0)
