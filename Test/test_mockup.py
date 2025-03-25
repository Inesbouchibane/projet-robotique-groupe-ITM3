import unittest
from unittest.mock import patch
from robot_mockup import RobotMockup

class TestRobotMockup(unittest.TestCase):
    
    def setUp(self):
        self.robot = RobotMockup("TestBot", 0, 0, 10, 20, 15, 5, "red")
    
    @patch("robot_mockup.uniform", return_value=0)
    
    def test_refresh_no_noise(self, mock_uniform):
        self.robot.setVitAng(1.0)
        self.robot.refresh(1.0)
        self.assertNotEqual((self.robot.x, self.robot.y), (0, 0))
        
    def test_getDistance(self):
        distance = self.robot.getDistance()
        self.assertTrue(10 <= distance <= 100)
        @patch("robot_mockup.uniform", return_value=0)
        
    def test_setVitAng(self, mock_uniform):
        self.robot.setVitAng(2.0)
        self.assertAlmostEqual(self.robot.vitAngD, 2.0, delta=0.05)
        self.assertAlmostEqual(self.robot.vitAngG, 2.0, delta=0.05)
    
if __name__ == "__main__":
    unittest.main()

    
