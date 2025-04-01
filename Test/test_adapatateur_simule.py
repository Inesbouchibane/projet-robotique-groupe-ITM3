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

    def test_set_vit_d(self):
        self.adaptateur.setVitD(6)
        self.robot.set_VitD.assert_called_once_with(6)
        self.robot.set_VitG.assert_not_called()

    def test_get_distance_obstacle_no_refresh(self):
        # Simuler un appel récent (moins de 0.06s)
        self.adaptateur.last_refresh = time() - 0.01
        self.adaptateur.last_dist = 50
        dist = self.adaptateur.getDistanceObstacle()
        self.assertEqual(dist, 50)  # Retourne la valeur mise en cache

    def test_get_distance_obstacle_with_refresh(self):
        # Simuler un appel après 0.06s
        self.adaptateur.last_refresh = time() - 0.07
        dist = self.adaptateur.getDistanceObstacle()
        # Calcul attendu : distance minimale entre les coins du robot et les points des obstacles
        # Robot à (0,0), taille 10x20, obstacles à (100,100), (100,110), (200,200)
        expected_dist = math.sqrt((100 - 5)**2 + (100 - 10)**2)  # Distance à (100,100)
        self.assertAlmostEqual(dist, expected_dist, delta=0.1)
        self.assertAlmostEqual(self.adaptateur.last_refresh, time(), delta=0.1)
        self.assertAlmostEqual(self.adaptateur.last_dist, expected_dist, delta=0.1)

    def test_get_distance_obstacle_no_obstacles(self):
        self.environnement.listeObs = []  # Aucun obstacle
        self.adaptateur.last_refresh = time() - 0.07
        dist = self.adaptateur.getDistanceObstacle()
        self.assertEqual(dist, 1000)  # Valeur par défaut si pas d'obstacles

    def test_get_distance_a(self):
        self.adaptateur.getDistanceObstacle = Mock(return_value=42)
        dist = self.adaptateur.getDistanceA()
        self.assertEqual(dist, 42)
        self.adaptateur.getDistanceObstacle.assert_called_once()

    def test_get_vit_d(self):
        self.robot.get_VitD.return_value = 7
        vit = self.adaptateur.getVitD()
        self.assertEqual(vit, 7)
        self.robot.get_VitD.assert_called_once()

    def test_get_vit_g(self):
        self.robot.get_VitG.return_value = -3
        vit = self.adaptateur.getVitG()
        self.assertEqual(vit, -3)
        self.robot.get_VitG.assert_called_once()

    def test_get_distance_parcourue(self):
        self.robot.getDistanceParcouru.return_value = 15
        dist = self.adaptateur.getDistanceParcourue()
        self.assertEqual(dist, 15)
        self.robot.getDistanceParcouru.assert_called_once()

    def test_get_angle_parcouru(self):
        self.robot.getAngleParcouru.return_value = math.pi / 2
        angle = self.adaptateur.getAngleParcouru()
        self.assertEqual(angle, math.pi / 2)
        self.robot.getAngleParcouru.assert_called_once()

    def test_get_position(self):
        self.robot.x = 5
        self.robot.y = -2
        pos = self.adaptateur.getPosition()
        self.assertEqual(pos, (5, -2))

    def test_get_direction(self):
        self.robot.direction = [0, 1]
        direction = self.adaptateur.getDirection()
        self.assertEqual(direction, [0, 1])

    def test_is_crashed_robot_crash(self):
        self.robot.estCrash = True
        self.adaptateur.getDistanceA = Mock(return_value=10)  # Pas trop proche
        self.assertTrue(self.adaptateur.isCrashed())

    def test_is_crashed_distance_too_close(self):
        self.robot.estCrash = False
        self.adaptateur.getDistanceA = Mock(return_value=4)  # Trop proche
        self.assertTrue(self.adaptateur.isCrashed())

    def test_is_crashed_no_crash(self):
        self.robot.estCrash = False
        self.adaptateur.getDistanceA = Mock(return_value=10)  # Pas trop proche
        self.assertFalse(self.adaptateur.isCrashed())

if __name__ == '__main__':
    unittest.main()
