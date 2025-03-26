import unittest
from unittest.mock import MagicMock
from .adapt import Adaptateur
from utils import getAngleFromVect, getDistanceFromPts
from .adaptateur_simule import Adaptateur_simule

class TestAdaptateurSimule(unittest.TestCase):
    def setUp(self):
        self.robot = MagicMock()
        self.robot.x = 0
        self.robot.y = 0
        self.robot.direction = 0
        self.robot.vitAngD = 0
        self.robot.vitAngG = 0
        
        self.env = MagicMock()
        self.adaptateur = Adaptateur_simule(self.robot, self.env)

    def test_initialisation(self):
        self.assertEqual(self.adaptateur.last_point, (0, 0))
        self.assertEqual(self.adaptateur.last_dir, 0)

    def test_initialise(self):
        self.robot.x = 10
        self.robot.y = 15
        self.robot.direction = 90
        self.adaptateur.initialise()
        self.assertEqual(self.adaptateur.last_point, (10, 15))
        self.assertEqual(self.adaptateur.last_dir, 90)

    def test_setVitAngDA(self):
        self.adaptateur.setVitAngDA(5)
        self.assertEqual(self.robot.vitAngD, 5)
    
    def test_setVitAngGA(self):
        self.adaptateur.setVitAngGA(3)
        self.assertEqual(self.robot.vitAngG, 3)
    
    def test_setVitAngA(self):
        self.robot.setVitAng = MagicMock()
        self.adaptateur.setVitAngA(7)
        self.robot.setVitAng.assert_called_once_with(7)

if __name__ == "__main__":
    unittest.main()
