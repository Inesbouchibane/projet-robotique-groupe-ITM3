import unittest
from unittest.mock import MagicMock
from time import time
from environnement import Environnement  # Assure-toi que ce module est bien importé

class TestEnvironnement(unittest.TestCase):
    def setUp(self):
        """Set up the environment for testing."""
        self.env = Environnement(width=100, length=100, scale=1)

    def test_initBorders(self):
        """Test if borders are initialized correctly."""
        self.env.initBorders()
        self.assertIn((0, 0), self.env.dicoObs)
        self.assertEqual(self.env.dicoObs[(0, 0)], 'bordure')

    def test_addObstacle(self):
        """Test if adding an obstacle works."""
        obstacle_points = [(10, 10), (20, 10), (20, 20), (10, 20)]
        self.env.addObstacle("obstacle1", obstacle_points)

        self.assertEqual(len(self.env.listeObs), 1)
        self.assertEqual(self.env.listeObs[0].nom, "obstacle1")

        for point in obstacle_points:
            scaled_point = (int(point[1] / self.env.scale), int(point[0] / self.env.scale))
            self.assertIn(scaled_point, self.env.dicoObs)
            self.assertEqual(self.env.dicoObs[scaled_point], "obstacle1")

    def test_verifCollision_no_collision(self):
        """Test if no collision is detected when there are no obstacles."""
        rob_mock = MagicMock()
        rob_mock.x = 50
        rob_mock.y = 50
        rob_mock.width = 10
        rob_mock.length = 10

        collision = self.env.verifCollision(rob_mock)
        self.assertFalse(collision)

    def test_verifCollision_with_collision(self):
        """Test if collision is detected with an obstacle."""
        rob_mock = MagicMock()
        rob_mock.x = 15
        rob_mock.y = 15
        rob_mock.width = 10
        rob_mock.length = 10

        obstacle_points = [(10, 10), (20, 10), (20, 20), (10, 20)]
        self.env.addObstacle("obstacle1", obstacle_points)

        collision = self.env.verifCollision(rob_mock)
        self.assertTrue(collision)

    def test_refreshEnvironnement_no_collision(self):
        """Test refreshing the environment when there is no collision."""
        rob_mock = MagicMock()
        rob_mock.robot = rob_mock  # Correction pour matcher l'implémentation
        rob_mock.estCrash = False
        rob_mock.refresh = MagicMock()

        self.env.setRobot(rob_mock)
        self.env.last_refresh = time()
        self.env.refreshEnvironnement()

        rob_mock.refresh.assert_called_once()

    def test_refreshEnvironnement_with_collision(self):
        """Test refreshing the environment when there is a collision."""
        rob_mock = MagicMock()
        rob_mock.robot = rob_mock  # Correction importante
        rob_mock.estCrash = False
        rob_mock.refresh = MagicMock()

        self.env.setRobot(rob_mock)

        obstacle_points = [(10, 10), (20, 10), (20, 20), (10, 20)]
        self.env.addObstacle("obstacle1", obstacle_points)

        rob_mock.x = 15
        rob_mock.y = 15
        rob_mock.width = 10
        rob_mock.length = 10

        self.env.last_refresh = time()
        self.env.refreshEnvironnement()

        self.assertTrue(rob_mock.estCrash)
        rob_mock.refresh.assert_not_called()

if __name__ == "__main__":
    unittest.main()


