# test_strategie.py
import unittest
from unittest.mock import MagicMock
import sys
import os

# Configuration des chemins
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controleur.strategies import (
    StrategieAvancer,
    StrategieTourner,
    VIT_ANG_AVAN,
    VIT_ANG_TOUR
)
from robot.robot import Robot
from environnement.Environnement import Environnement

class TestStrategieAvancer(unittest.TestCase):
    def setUp(self):
        # Paramètres CORRECTS pour Environnement (width, length, scale)
        self.env = Environnement(width=800, length=600, scale=1)
        
        # Paramètres CORRECTS pour Robot (nom, x, y, width, length, height, rayonRoue, couleur)
        self.robot = Robot(
            nom="RobotTest",
            x=0, 
            y=0,
            width=20,
            length=30,
            height=10,
            rayonRoue=5,
            couleur='red'
        )
        self.robot.env = self.env  # Lien manuel si nécessaire
        self.adaptateur_mock = MagicMock()
        self.adaptateur_mock.robot = self.robot
        self.strategie = StrategieAvancer(self.adaptateur_mock, 100)

    def test_arret_distance(self):
        self.strategie.start_position = (0, 0)
        self.robot.y = 99
        self.assertFalse(self.strategie.stop())
        
        self.robot.y = 101
        self.assertTrue(self.strategie.stop())

class TestStrategieTourner(unittest.TestCase):
    def setUp(self):
        self.env = Environnement(width=800, length=600, scale=1)
        self.robot = Robot(
            nom="RobotTourner",
            x=0,
            y=0,
            width=20,
            length=30,
            height=10,
            rayonRoue=5,
            couleur='blue'
        )
        self.robot.env = self.env
        self.adaptateur_mock = MagicMock()
        self.adaptateur_mock.robot = self.robot
        self.strategie = StrategieTourner(self.adaptateur_mock, 90)

    def test_rotation_complete(self):
        self.strategie.start()
        self.adaptateur_mock.setVitAngGA.assert_called_with(-VIT_ANG_TOUR)
        self.adaptateur_mock.setVitAngDA.assert_called_with(VIT_ANG_TOUR)

# ... (Adaptez de même pour les autres tests)
