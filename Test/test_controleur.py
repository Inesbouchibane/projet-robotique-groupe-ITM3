import unittest
from unittest.mock import MagicMock, patch
from controleur import Controleur

class TestControleur(unittest.TestCase):

    def setUp(self):
        # Initialisation des paramètres pour le contrôleur
        self.vitesse_gauche = 1.0
        self.vitesse_droite = 1.0
        self.mode = "test"
        self.controleur = Controleur(self.vitesse_gauche, self.vitesse_droite, self.mode, affichage=False)

    def test_initialisation(self):
        # Vérifie que le contrôleur est correctement initialisé
        self.assertEqual(self.controleur.vitesse_gauche_initiale, self.vitesse_gauche)
        self.assertEqual(self.controleur.vitesse_droite_initiale, self.vitesse_droite)
        self.assertEqual(self.controleur.env.mode, self.mode)

    def test_ajuster_vitesse(self):
        # Teste la méthode ajuster_vitesse
        nouvelle_vg = 2.0
        nouvelle_vd = 2.0
        self.controleur.ajuster_vitesse(nouvelle_vg, nouvelle_vd)
        self.assertEqual(self.controleur.env.robot.vitesse_gauche, nouvelle_vg)
        self.assertEqual(self.controleur.env.robot.vitesse_droite, nouvelle_vd)
