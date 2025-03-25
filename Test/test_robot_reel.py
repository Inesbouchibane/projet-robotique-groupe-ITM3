import unittest
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Code/robot')))

from robot_reel import RobotReel  

# Simulons un capteur de distance pour les tests
class CapteurDistanceSimule:
    def __init__(self, distance):
        self.distance = distance
    
    def mesurer_distance(self):
        """Retourne une distance simulée."""
        return self.distance

class TestRobotReel(unittest.TestCase):

    def setUp(self):
        """Initialise un robot réel pour chaque test."""
        # Création d'une instance de RobotReel avec des valeurs d'exemple
        self.robot = RobotReel(nom="Robot1", x=0, y=0, width=30, length=40, height=50, rayonRoue=10, couleur="rouge")

    def test_initialisation_robot(self):
        """Test l'initialisation des attributs du robot."""
        self.assertEqual(self.robot.nom, "Robot1")
        self.assertEqual(self.robot.x, 0)
        self.assertEqual(self.robot.y, 0)
        self.assertEqual(self.robot.width, 30)
        self.assertEqual(self.robot.length, 40)
        self.assertEqual(self.robot.height, 50)
        self.assertEqual(self.robot.rayonRoue, 10)
        self.assertEqual(self.robot.couleur, "rouge")
        self.assertIsNone(self.robot.capteur_distance)  # Le capteur doit être None par défaut

    def test_setMoteurDPS(self):
      """Test de la méthode setMoteurDPS."""
        # Définir la vitesse des moteurs
        self.robot.setMoteurDPS(90, 120)
        
        # Vérification des vitesses angulaires définies
        self.assertEqual(self.robot.vitAngG, 90)
        self.assertEqual(self.robot.vitAngD, 120)

    def test_getDistance_sans_capteur(self):
        """Test de la méthode getDistance sans capteur."""
        # Vérifier que la méthode retourne 'inf' si aucun capteur n'est défini
        distance = self.robot.getDistance()
        self.assertEqual(distance, float('inf'))

    def test_getDistance_avec_capteur(self):
        """Test de la méthode getDistance avec un capteur."""
        # Ajouter un capteur de distance simulé
        capteur = CapteurDistanceSimule(15.5)
        self.robot.capteur_distance = capteur
        
        # Vérification que la méthode retourne la distance mesurée par le capteur
        distance = self.robot.getDistance()
        self.assertEqual(distance, 15.5)

if __name__ == "__main__":
    unittest.main()
