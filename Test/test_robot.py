import unittest
from robot import Robot

class TestRobot(unittest.TestCase):
    def setUp(self):
        """Initialisation d'un robot avant chaque test."""
        self.robot = Robot(100, 100, 10, 10)  # Position initiale avec vitesse gauche = droite = 10
    
    def test_deplacement(self):
        x_avant, y_avant = self.robot.x, self.robot.y
        self.robot.deplacer()
        self.assertNotEqual((self.robot.x, self.robot.y), (x_avant, y_avant))


    def test_limite_fenetre(self):
        """Test que le robot ne sort pas des limites (0,800)x(0,600)."""
        self.robot.x = 795
        self.robot.y = 595
        self.robot.vitesse_gauche = 10
        self.robot.vitesse_droite = 10
        self.robot.deplacer()
        self.assertLessEqual(self.robot.x, 800)
        self.assertLessEqual(self.robot.y, 600)

    
    def test_scan_infrarouge(self):
        """Test du capteur infrarouge avec un obstacle."""
        obstacles = [(200, 200, 50, 50)]
        point_detecte = self.robot.scan_infrarouge(obstacles, 100)
        self.assertIsInstance(point_detecte, tuple) # Vérifie que c'est un tuple
        self.assertEqual(len(point_detecte), 2) # Vérifie qu'il contient bien (x, y)

if __name__ == "__main__":
    unittest.main()

