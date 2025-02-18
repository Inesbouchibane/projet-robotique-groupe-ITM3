import unittest
import math
from robot import Robot

class TestRobot(unittest.TestCase):
    def setUp(self):
        self.robot = Robot(100, 100, 1, 1)
    
    def test_deplacement(self):
        x_avant, y_avant = self.robot.x, self.robot.y
        self.robot.deplacer()
        self.assertNotEqual((self.robot.x, self.robot.y), (x_avant, y_avant))
        self.assertAlmostEqual(self.robot.x, x_avant + 10, delta=0.1)
        self.assertAlmostEqual(self.robot.y, y_avant, delta=0.1) 
        
    def test_rotation(self):
        self.robot.vitesse_gauche = 5
        self.robot.vitesse_droite = 10
        angle_avant = self.robot.angle
        self.robot.deplacer()
        self.assertNotEqual(self.robot.angle, angle_avant) 

        
    def test_scan_infrarouge(self):
        obstacles = [(200, 200, 50, 50)]
        point_detecte = self.robot.scan_infrarouge(obstacles, 100)
        self.assertIsInstance(point_detecte, tuple)
        self.assertEqual(len(point_detecte), 2)

if __name__ == "__main__":
    unittest.main()

