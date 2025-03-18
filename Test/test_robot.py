import unittest
import math
from robot.robot import Robot  
from utils import VIT_ANG_TOUR  

class TestRobot(unittest.TestCase):
    def setUp(self):
        # Initialisation du robot avec les paramètres nécessaires
        self.robot = Robot(nom="TestRobot", x=100, y=100, width=20, length=30, height=10, rayonRoue=5, couleur="blue")
    
    def test_deplacement_ligne_droite(self):
        # Test du déplacement en ligne droite
        x_avant, y_avant = self.robot.x, self.robot.y
        self.robot.setVitAng(1)  # Définir une vitesse angulaire égale pour les deux roues
        self.robot.refresh(1) 
        self.assertNotEqual((self.robot.x, self.robot.y), (x_avant, y_avant))
        # Vérification que le robot s'est déplacé dans la direction actuelle
        self.assertAlmostEqual(self.robot.x, x_avant + self.robot.direction[0] * self.robot.getVitesse(), delta=0.1)
        self.assertAlmostEqual(self.robot.y, y_avant + self.robot.direction[1] * self.robot.getVitesse(), delta=0.1)

    def test_rotation(self):
        # Test de la rotation du robot
        self.robot.vitAngG = 5  # Vitesse angulaire de la roue gauche
        self.robot.vitAngD = 10  # Vitesse angulaire de la roue droite
        angle_avant = self.robot.getAngle()
        self.robot.refresh(1)  # Simuler un déplacement pendant 1 seconde
        self.assertNotEqual(self.robot.getAngle(), angle_avant)
        # Vérification que l'angle a changé selon la différence de vitesse des roues
        delta_angle = (self.robot.getVitesseD() - self.robot.getVitesseG()) / self.robot.width
        self.assertAlmostEqual(self.robot.getAngle(), (angle_avant + delta_angle) % (2 * math.pi), delta=0.1)
    
    def test_getDistance(self):
        # Test de la méthode getDistance (simulation d'un environnement avec un obstacle)
        class MockEnv:
            def __init__(self):
                self.scale = 1
                self.dicoObs = {(105, 100): True}  
        
        env = MockEnv()
        distance = self.robot.getDistance(env)
        self.assertAlmostEqual(distance, 5, delta=0.1)  # Vérification que la distance est correcte

    def test_avoidObstacle(self):
        # Test de la méthode avoidObstacle
        class MockEnv:
            def __init__(self):
                self.scale = 1
                self.dicoObs = {(105, 100): True} 
        
        env = MockEnv()
        self.robot.avoidObstacle(env)
        # Vérification que les vitesses des roues ont été modifiées pour éviter l'obstacle
        self.assertEqual(self.robot.vitAngG, -VIT_ANG_TOUR)
        self.assertEqual(self.robot.vitAngD, VIT_ANG_TOUR)

if __name__ == "__main__":
    unittest.main()
