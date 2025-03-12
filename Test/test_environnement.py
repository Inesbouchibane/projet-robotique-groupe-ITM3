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

