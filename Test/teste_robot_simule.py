import unittest
from time import sleep
from src.robot_simule import RobotSimule

class TestRobotSimule(unittest.TestCase):

    def setUp(self):
        self.robot = RobotSimule("TestBot", x=0, y=0, width=20, length=30, vitesse_max=10, taille_roue=5)
        
        
    def test_initialisation(self):
        self.assertEqual(self.robot.nom, "TestBot")
        self.assertEqual(self.robot.x, 0)
        self.assertEqual(self.robot.y, 0)
        self.assertEqual(self.robot.width, 20)
        self.assertEqual(self.robot.length, 30)
        self.assertEqual(self.robot.vitesse_max, 10)
        self.assertEqual(self.robot.taille_roue, 5)
        self.assertEqual(self.robot.couleur, "lightblue")
        self.assertEqual(self.robot.direction, [1, 0])
        self.assertEqual(self.robot.vitAngG, 0)
        self.assertEqual(self.robot.vitAngD, 0)
        self.assertEqual(self.robot.distance_parcourue, 0)
        self.assertEqual(self.robot.angle_parcouru, 0)
        self.assertFalse(self.robot.estCrash)
