import unittest
from adapt import Adaptateur_simule
from utils import getDistanceFromPts, getAngleFromVect

class MockRobot:
    def __init__(self, x=0, y=0, direction=0):
        self.x = x
        self.y = y
        self.direction = direction
        self.vitAngD = 0
        self.vitAngG = 0

    def setVitAng(self, vit):
        self.vitAngD = vit
        self.vitAngG = vit

    def getDistance(self, env):
        return 10  # Valeur arbitraire pour le test

class MockEnv:
    pass

class TestAdaptateurSimule(unittest.TestCase):
    def setUp(self):
        self.robot = MockRobot()
        self.env = MockEnv()
        self.adaptateur = Adaptateur_simule(self.robot, self.env)

    def test_initialise(self):
        self.robot.x, self.robot.y, self.robot.direction = 5, 5, 90
        self.adaptateur.initialise()
        self.assertEqual(self.adaptateur.last_point, (5, 5))
        self.assertEqual(self.adaptateur.last_dir, 90)

    def test_setVitAngA(self):
        self.adaptateur.setVitAngA(30)
        self.assertEqual(self.robot.vitAngD, 30)
        self.assertEqual(self.robot.vitAngG, 30)

    def test_getDistanceA(self):
        self.assertEqual(self.adaptateur.getDistanceA(), 10)

    def test_getDistanceParcourue(self):
        self.robot.x, self.robot.y = 3, 4
        self.adaptateur.last_point = (0, 0)
        expected_distance = getDistanceFromPts((3, 4), (0, 0))
        self.assertEqual(self.adaptateur.getDistanceParcourue(), expected_distance)

    def test_getAngleParcouru(self):
        self.robot.direction = 45
        self.adaptateur.last_dir = 0
        expected_angle = getAngleFromVect(0, 45)
        self.assertEqual(self.adaptateur.getAngleParcouru(), expected_angle)

if __name__ == "__main__":
    unittest.main()
