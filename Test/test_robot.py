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
