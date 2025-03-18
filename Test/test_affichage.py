import unittest
from unittest.mock import MagicMock, patch
import pygame
from affichage import Affichage

# Constantes pour simuler l'environnement
LARGEUR = 800
HAUTEUR = 600
OBSTACLES = [(200, 200, 100, 100), (400, 300, 50, 50)]

class TestAffichage(unittest.TestCase):

    def setUp(self):
        """Initialisation avant chaque test."""
        pygame.init()
        pygame.display.set_mode((1, 1))  # Mode d'affichage minimal pour éviter l'erreur "Display mode not set"

        self.affichage = Affichage(LARGEUR, HAUTEUR, OBSTACLES)

        # Simulation d'un robot
        self.robot = MagicMock()
        self.robot.x = LARGEUR / 2
        self.robot.y = HAUTEUR / 2
        self.robot.width = 20
        self.robot.length = 20
        self.robot.direction = (1, 0)
        self.robot.estCrash = False

        self.affichage.ecran = pygame.Surface((LARGEUR, HAUTEUR))

    def tearDown(self):
        """Nettoyage après chaque test pour éviter les conflits."""
        pygame.quit()

    def test_handle_events_quit(self):
        """Test de l'événement 'QUIT'."""
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        action = self.affichage.handle_events(None)
        self.assertEqual(action, "quit")

    def test_handle_events_tracer_carre(self):
        """Test de l'événement 'tracer_carre'."""
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c))
        action = self.affichage.handle_events(None)
        self.assertEqual(action, "tracer_carre")

    def test_handle_events_automatique(self):
        """Test de l'événement 'automatique'."""
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a))
        action = self.affichage.handle_events(None)
        self.assertEqual(action, "automatique")

    def test_mettre_a_jour(self):
        """Test de la mise à jour de l'affichage."""
        self.affichage.mettre_a_jour(self.robot)
        self.assertGreater(len(self.affichage.trajet), 0, "Le trajet du robot devrait être mis à jour.")

    def test_calculer_points_robot(self):
        """Test du calcul des points du robot."""
        points = self.affichage.calculer_points_robot(self.robot)
        self.assertEqual(len(points), 4, "Le robot doit être représenté par un quadrilatère.")

    def test_attendre_fermeture(self):
        """Test de la fermeture de l'affichage."""
        with patch("pygame.event.get", return_value=[pygame.event.Event(pygame.QUIT)]):
            with patch("pygame.quit") as mock_quit:
                self.affichage.attendre_fermeture()
                mock_quit.assert_called_once()

if __name__ == "__main__":
    unittest.main()

