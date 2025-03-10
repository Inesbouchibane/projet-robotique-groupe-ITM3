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
    
    def test_limite_fenetre(self):
        self.robot.x = 795
        self.robot.y = 595
        self.robot.vitesse_gauche = 10
        self.robot.vitesse_droite = 10
        self.robot.deplacer()
        # Vérification que le robot ne bouge pas car il est déjà à la limite
        self.assertEqual(self.robot.x, 795)
        self.assertEqual(self.robot.y, 595)
    def test_scan_infrarouge(self):
        obstacles = [(200, 200, 50, 50)]
        point_detecte = self.robot.scan_infrarouge(obstacles, 100)
        self.assertIsInstance(point_detecte, tuple)
        self.assertEqual(len(point_detecte), 2)
        # Vérification que le point détecté est bien dans l'obstacle
        if point_detecte != (self.robot.x + 100 * math.cos(math.radians(self.robot.angle)),
                            self.robot.y - 100 * math.sin(math.radians(self.robot.angle))):
            self.assertTrue(200 <= point_detecte[0] <= 250 and 200 <= point_detecte[1] <= 250)

if __name__ == "__main__":
    unittest.main()
