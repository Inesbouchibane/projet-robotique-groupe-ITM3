import unittest
from unittest.mock import MagicMock
from controleur import Controleur
from environnement import Environnement

class TestControleur(unittest.TestCase):
    
    def setUp(self):
        self.env_mock = MagicMock(spec=Environnement)  # Mock de l'environnement
        self.env_mock.robot = MagicMock()  # Mock du robot
	self.env_mock.demarrer_simulation = MagicMock()  # Mock de demarrer_simulation
        self.controleur = Controleur(5, 5, "automatique")
        self.controleur.env = self.env_mock  # Remplace l'environnement réel par un mock
    
    def test_demarrer_simulation(self):
        """ Test du démarrage de la simulation """
        self.controleur.demarrer_simulation()
        # Vérifie que la méthode demarrer_simulation a bien été appelée sur l'objet env_mock
        self.env_mock.demarrer_simulation.assert_called_once() 

    def test_ajuster_vitesse(self):
        """ Test de l'ajustement des vitesses """
        self.controleur.ajuster_vitesse(3, 4)
        # Vérifie que les vitesses ont été correctement ajustées
        self.assertEqual(self.controleur.env.robot.vitesse_gauche, 3)
        self.assertEqual(self.controleur.env.robot.vitesse_droite, 4)
 

if __name__ == "__main__":
    unittest.main()