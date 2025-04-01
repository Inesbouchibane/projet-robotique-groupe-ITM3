import unittest
from time import sleep
from src.robot_simule import RobotSimule

class TestRobotSimule(unittest.TestCase):

    def setUp(self):
        self.robot = RobotSimule("TestBot", x=0, y=0, width=20, length=30, vitesse_max=10, taille_roue=5)
