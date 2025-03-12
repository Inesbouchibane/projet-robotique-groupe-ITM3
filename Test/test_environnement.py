import unittest
from unittest.mock import MagicMock
from environnement import Environnement
from robot import Robot

class TestEnvironnement(unittest.TestCase):

    def setUp(self):
        """
        Initialisation avant chaque test.
        """
        # Crée un environnement avec des vitesses par défaut et mode manuel
        self.env = Environnement(vitesse_gauche=2, vitesse_droite=2, mode="manuel", affichage=False)
        self.robot = self.env.robot

    def test_collision_detection(self):
        """
        Tester la détection de collision avec un obstacle.
        """
        # Ajouter un obstacle à une position spécifique
        self.env.obstacles.append((100, 100, 50, 50))  # Un obstacle à (100, 100) de taille 50x50
        
        # Placer le robot à une position proche de l'obstacle
        self.robot.x, self.robot.y = 120, 120
        
        # Vérifier que la détection de collision retourne True
        self.assertTrue(self.env.detecter_collision(self.robot.x, self.robot.y))
        
        # Placer le robot loin de l'obstacle
        self.robot.x, self.robot.y = 200, 200
        
        # Vérifier que la détection de collision retourne False
        self.assertFalse(self.env.detecter_collision(self.robot.x, self.robot.y))

    def test_no_collision(self):
        """
        Tester la situation où il n'y a pas de collision.
        """
        self.env.obstacles.append((200, 200, 50, 50))  # Ajouter un obstacle
        self.robot.x, self.robot.y = 500, 500  # Positionner le robot loin de l'obstacle
        self.assertFalse(self.env.detecter_collision(self.robot.x, self.robot.y))

    def test_mouvement_robot(self):
        """
        Tester le mouvement du robot.
        """
        # Sauvegarder la position initiale du robot
        initial_x, initial_y = self.robot.x, self.robot.y

        # Déplacer le robot
        self.robot.deplacer()

        # Vérifier que la position a changé après le déplacement
        self.assertNotEqual(self.robot.x, initial_x)
        self.assertNotEqual(self.robot.y, initial_y)

    def test_automatic_mode_obstacle_detection(self):
        """
        Tester le mode automatique et la détection d'obstacles.
        """
        # Ajouter un obstacle à une position spécifique
        self.env.obstacles.append((100, 100, 50, 50))
        
        # Positionner le robot assez proche de l'obstacle
        self.robot.x, self.robot.y = 110, 110
        
        # Simuler un scan infrarouge pour détecter l'obstacle
        ir_point = self.robot.scan_infrarouge(self.env.obstacles, 100)
        distance_ir = ((ir_point[0] - self.robot.x) ** 2 + (ir_point[1] - self.robot.y) ** 2) ** 0.5

        # Vérifier que la distance IR est bien inférieure à 100
        self.assertLess(distance_ir, 100)

    def test_update_position_on_collision(self):
        """
        Tester si la position du robot ne change pas après une collision.
        """
        # Sauvegarder la position initiale du robot
        initial_x, initial_y = self.robot.x, self.robot.y
        
        # Ajouter un obstacle à la position de départ du robot
        self.env.obstacles.append((initial_x, initial_y, 50, 50))
        
        # Déplacer le robot
        self.robot.deplacer()

        # Vérifier que la position du robot n'a pas changé
        self.assertEqual(self.robot.x, initial_x)
        self.assertEqual(self.robot.y, initial_y)

if __name__ == '__main__':
    unittest.main()


