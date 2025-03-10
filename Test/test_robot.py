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
        self.assertAlmostEqual(self.robot.x, x_avant + 1, delta=0.1)  # Correction ici
        self.assertAlmostEqual(self.robot.y, y_avant, delta=0.1) 
        
    def test_rotation(self):
        self.robot.vitesse_gauche = 5
        self.robot.vitesse_droite = 10
        angle_avant = self.robot.angle
        self.robot.deplacer()
        self.assertNotEqual(self.robot.angle, angle_avant)
        # Vérification plus précise de l'angle
        delta_angle = (self.robot.vitesse_droite - self.robot.vitesse_gauche) / self.robot.largeur * 10
        self.assertAlmostEqual(self.robot.angle, (angle_avant + delta_angle) % 360, delta=0.1)
    
