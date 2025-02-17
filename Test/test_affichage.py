import unittest
from unittest.mock import MagicMock, patch
import pygame
from affichage import Affichage
from robot import Robot
import math

# Constantes pour simuler l'environnement
LARGEUR = 800
HAUTEUR = 600
OBSTACLES = [(200, 200, 100, 100), (400, 300, 50, 50)]  # Liste d'obstacles

class TestAffichage(unittest.TestCase):

    @patch("pygame.display.set_mode")
    @patch("pygame.font.SysFont")
    def setUp(self, mock_font, mock_set_mode):
        """
        Initialisation avant chaque test.
        On mock pygame.display et pygame.font pour éviter de lancer la fenêtre Pygame.
        """
        # Mock pygame
        mock_set_mode.return_value = MagicMock()
        mock_font.return_value = MagicMock()
        
        # Création de l'objet Affichage
        self.affichage = Affichage(LARGEUR, HAUTEUR, OBSTACLES)
        
        # Création du robot
        self.robot = Robot(LARGEUR / 2, HAUTEUR / 2, 2, 2)
        
        # Mock des méthodes Pygame
        self.affichage.ecran = MagicMock()
        self.affichage.clock = MagicMock()
    def test_handle_events_quit(self):
        """Test de la gestion de l'événement 'QUIT'."""
        # Simuler un événement QUIT
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        action = self.affichage.handle_events()
        self.assertEqual(action, "quit")

    def test_handle_events_stop(self):
        """Test de la gestion de l'événement 'stop'."""
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s))
        action = self.affichage.handle_events()
        self.assertEqual(action, "stop")
    

    def test_handle_events_change(self):
        """Test de la gestion de l'événement 'change'."""
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d))
        action = self.affichage.handle_events()
        self.assertEqual(action, "change")
