import unittest
from unittest.mock import Mock
import math
from time import time
from robot.adapt_simule import AdaptateurSimule
from robot.robot_simule import RobotSimule
from environnement import Environnement

class TestAdaptateurSimule(unittest.TestCase):
    def setUp(self):
        # Créer des mocks pour RobotSimule et Environnement
        self.robot = Mock(spec=RobotSimule)
        self.robot.x = 0
        self.robot.y = 0
        self.robot.width = 10
        self.robot.length = 20
        self.robot.direction = [1, 0]  # Direction initiale : droite
        self.robot.estCrash = False

        self.environnement = Mock(spec=Environnement)
        self.environnement.listeObs = [
            Mock(points=[(100, 100), (100, 110)]),  # Obstacle 1
            Mock(points=[(200, 200)])               # Obstacle 2
        ]

        # Initialiser l'adaptateur
        self.adaptateur = AdaptateurSimule(self.robot, self.environnement)
        
        # Configurer les valeurs par défaut des mocks
        self.robot.get_VitG.return_value = 0
        self.robot.get_VitD.return_value = 0
        self.robot.getDistanceParcouru.return_value = 0
        self.robot.getAngleParcouru.return_value = 0

    def test_initialise(self):
        self.adaptateur.initialise()
        self.robot.arreter.assert_called_once()
        self.robot.reset_tracking.assert_called_once()
        self.assertTrue(self.adaptateur.initialised)
        self.assertAlmostEqual(self.adaptateur.last_refresh, time(), delta=0.1)

    def test_set_vit_ang_a(self):
        self.adaptateur.setVitAngA(5)
        self.robot.set_VitG.assert_called_once_with(5)
        self.robot.set_VitD.assert_called_once_with(5)

    def test_set_vit_ang_ga(self):
        self.adaptateur.setVitAngGA(3)
        self.robot.set_VitG.assert_called_once_with(3)
        self.robot.set_VitD.assert_not_called()

    def test_set_vit_ang_da(self):
        self.adaptateur.setVitAngDA(-2)
        self.robot.set_VitD.assert_called_once_with(-2)
        self.robot.set_VitG.assert_not_called()

    def test_set_vit_g(self):
        self.adaptateur.setVitG(4)
        self.robot.set_VitG.assert_called_once_with(4)
        self.robot.set_VitD.assert_not_called()
