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
        
    def test_avancer(self):
        self.robot.avancer(5)
        self.assertEqual(self.robot.vitAngG, 2.0)
        self.assertEqual(self.robot.vitAngD, 2.0)

    def test_arreter(self):
        self.robot.avancer(5)
        self.robot.arreter()
        self.assertEqual(self.robot.vitAngG, 0)
        self.assertEqual(self.robot.vitAngD, 0)
        
    def test_set_vitesses(self):
        self.robot.set_VitG(3)
        self.robot.set_VitD(4)
        self.assertEqual(self.robot.get_VitG(), 3)
        self.assertEqual(self.robot.get_VitD(), 4)

    def test_get_distance_parcourue(self):
        self.assertEqual(self.robot.getDistanceParcouru(), 0)
        
    def test_get_angle_parcouru(self):
        self.assertEqual(self.robot.getAngleParcouru(), 0)

    def test_refresh(self):
        self.robot.avancer(5)
        sleep(0.05)  # Simulation du temps écoulé
        self.robot.refresh()
        self.assertGreater(self.robot.getDistanceParcouru(), 0)
        self.assertGreater(self.robot.getAngleParcouru(), 0)

