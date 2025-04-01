import unittest
from unittest.mock import Mock
import math
from controleur.strategies import (StrategieAvancer, StrategieTourner, StrategieSeq, 
                                   StrategieAuto, setStrategieCarre, StrategieSuivreBalise)

class TestStrategies(unittest.TestCase):
    def setUp(self):
        # Créer un mock pour l'adaptateur
        self.adaptateur = Mock()
        self.adaptateur.getDistanceParcourue.return_value = 0
        self.adaptateur.getAngleParcouru.return_value = 0
        self.adaptateur.getDistanceA.return_value = 100  # Pas d'obstacle proche par défaut
        self.adaptateur.getPosition.return_value = (0, 0)
        self.adaptateur.getDirection.return_value = [1, 0]  # Direction initiale : droite
        self.adaptateur.robot.direction = [1, 0]  # Simuler la direction du robot

    # Tests pour StrategieAvancer
    def test_strategie_avancer_start(self):
        strat = StrategieAvancer(50)
        strat.start(self.adaptateur)
        self.adaptateur.initialise.assert_called_once()
        self.adaptateur.setVitAngA.assert_called_once_with(2)  # VIT_ANG_AVAN = 2
        self.assertEqual(strat.parcouru, 0)

    def test_strategie_avancer_stop_obstacle(self):
        strat = StrategieAvancer(50)
        self.adaptateur.getDistanceA.return_value = 10  # Obstacle proche
        strat.start(self.adaptateur)
        self.assertTrue(strat.stop(self.adaptateur))
        self.adaptateur.setVitAngA.assert_called_with(0)

    def test_strategie_avancer_stop_distance(self):
        strat = StrategieAvancer(50)
        self.adaptateur.getDistanceParcourue.return_value = 60
        strat.start(self.adaptateur)
        strat.step(self.adaptateur)  # Mettre à jour parcouru
        self.assertTrue(strat.stop(self.adaptateur))
        self.adaptateur.setVitAngA.assert_called_with(0)

    # Tests pour StrategieTourner
    def test_strategie_tourner_start_left(self):
        strat = StrategieTourner(90)
        strat.start(self.adaptateur)
        self.adaptateur.setVitAngGA.assert_called_once_with(-1)  # VIT_ANG_TOUR = 1
        self.adaptateur.setVitAngDA.assert_called_once_with(1)
        self.assertEqual(strat.angle_parcouru, 0)

    def test_strategie_tourner_stop_angle(self):
        strat = StrategieTourner(90)
        self.adaptateur.getAngleParcouru.return_value = math.radians(91)
        strat.start(self.adaptateur)
        strat.step(self.adaptateur)
        self.assertTrue(strat.stop(self.adaptateur))
        self.adaptateur.setVitAngGA.assert_called_with(0)
        self.adaptateur.setVitAngDA.assert_called_with(0)

    def test_strategie_tourner_snap_direction(self):
        strat = StrategieTourner(90)
        self.adaptateur.getAngleParcouru.return_value = math.radians(90)
        self.adaptateur.getDirection.return_value = [0, 1]  # Après rotation
        strat.start(self.adaptateur)
        strat.step(self.adaptateur)
        strat.stop(self.adaptateur)
        self.assertEqual(self.adaptateur.robot.direction, [0, 1])  # Direction ajustée

    # Tests pour StrategieSeq
    def test_strategie_seq_execution(self):
        # Créer des mocks pour les stratégies internes
        strat1 = Mock(spec=StrategieAvancer)
        strat2 = Mock(spec=StrategieTourner)
        strat_seq = StrategieSeq([strat1, strat2])
        
        # Simuler le comportement
        strat_seq.start(self.adaptateur)
        strat1.start.assert_called_once_with(self.adaptateur)
        
        strat_seq.step(self.adaptateur)
        strat1.step.assert_called_once_with(self.adaptateur)
        
        strat1.stop.return_value = True  # Simuler que strat1 est terminé
        strat_seq.step(self.adaptateur)  # Passe à strat2
        strat2.start.assert_called_once_with(self.adaptateur)

    def test_strategie_seq_stop(self):
        strat = StrategieSeq([StrategieAvancer(10)])
        strat.index = 1  # Simuler que toutes les stratégies sont terminées
        self.assertTrue(strat.stop(self.adaptateur))

    # Tests pour StrategieAuto
    def test_strategie_auto_start(self):
        strat = StrategieAuto(5, -5)
        strat.start(self.adaptateur)
        self.adaptateur.setVitAngGA.assert_called_once_with(5)
        self.adaptateur.setVitAngDA.assert_called_once_with(-5)

    def test_strategie_auto_no_stop(self):
        strat = StrategieAuto(5, -5)
        strat.start(self.adaptateur)
        self.assertFalse(strat.stop(self.adaptateur))  # Ne s'arrête pas automatiquement

    # Tests pour setStrategieCarre
    def test_set_strategie_carre(self):
        strat = setStrategieCarre(100)
        self.assertIsInstance(strat, StrategieSeq)
        self.assertEqual(len(strat.liste_strategies), 8)
        self.assertIsInstance(strat.liste_strategies[0], StrategieAvancer)
        self.assertEqual(strat.liste_strategies[0].distance, 100)
        self.assertIsInstance(strat.liste_strategies[1], StrategieTourner)
        self.assertEqual(strat.liste_strategies[1].angle_cible, math.radians(90))

    # Tests pour StrategieSuivreBalise
    def test_strategie_suivre_balise_start(self):
        strat = StrategieSuivreBalise((100, 100))
        strat.start(self.adaptateur)
        self.adaptateur.initialise.assert_called_once()
        self.assertEqual(strat.distance_parcourue, 0)

    def test_strategie_suivre_balise_turn(self):
        strat = StrategieSuivreBalise((100, 0))  # Balise à droite
        strat.start(self.adaptateur)
        strat.step(self.adaptateur)
        self.assertTrue(self.adaptateur.setVitAngGA.called)
        self.assertTrue(self.adaptateur.setVitAngDA.called)

    def test_strategie_suivre_balise_stop_obstacle(self):
        strat = StrategieSuivreBalise((100, 100))
        self.adaptateur.getDistanceA.return_value = 10  # Obstacle proche
        strat.start(self.adaptateur)
        self.assertTrue(strat.stop(self.adaptateur))
        self.adaptateur.setVitAngGA.assert_called_with(0)
        self.adaptateur.setVitAngDA.assert_called_with(0)

    def test_strategie_suivre_balise_stop_arrival(self):
        strat = StrategieSuivreBalise((5, 0))
        self.adaptateur.getPosition.return_value = (4, 0)  # Proche de la balise
        strat.start(self.adaptateur)
        self.assertTrue(strat.stop(self.adaptateur))
        self.adaptateur.setVitAngGA.assert_called_with(0)
        self.adaptateur.setVitAngDA.assert_called_with(0)

if __name__ == '__main__':
    unittest.main()
