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

    
      @patch('controleur.Controleur.tourner')
    def test_tourner(self, mock_tourner):
        # Teste la méthode tourner avec un angle de 90 degrés
        angle = 90
        mock_tourner.return_value = True
        result = self.controleur.tourner(angle)
        self.assertTrue(result)
        mock_tourner.assert_called_once_with(angle)

    @patch('controleur.Controleur.avancer')
    def test_avancer(self, mock_avancer):
        # Teste la méthode avancer avec une distance de 100 unités
        distance = 100
        mock_avancer.return_value = True
        result = self.controleur.avancer(distance)
        self.assertTrue(result)
        mock_avancer.assert_called_once_with(distance)

    @patch('controleur.Controleur.tracer_carre')
    def test_tracer_carre(self, mock_tracer_carre):
        # Teste la méthode tracer_carre avec un côté de 200 unités
        cote = 200
        self.controleur.tracer_carre(cote)
        mock_tracer_carre.assert_called_once_with(cote)

    @patch('controleur.Controleur.avancer_vers_mur_proche')
    def test_avancer_vers_mur_proche(self, mock_avancer_vers_mur_proche):
        # Teste la méthode avancer_vers_mur_proche
        self.controleur.avancer_vers_mur_proche()
        mock_avancer_vers_mur_proche.assert_called_once()

    @patch('controleur.Controleur.executer_strategies')
    def test_executer_strategies(self, mock_executer_strategies):
        # Teste la méthode executer_strategies
        strategies = [("avancer", {"distance": 100}), ("tourner", {"angle": 90})]
        self.controleur.executer_strategies(strategies)
        mock_executer_strategies.assert_called_once_with(strategies)

if __name__ == '__main__':
    unittest.main()
