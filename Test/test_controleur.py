import unittest
from unittest.mock import MagicMock, patch
from controleur import Controler
from time import sleep
from utils import TIC_SIMULATION

class TestControler(unittest.TestCase):
    def setUp(self):
        self.controler = Controler()
        self.controler.running = False  # Empêcher le thread de tourner en test
        
    def tearDown(self):
        self.controler.running = False

    def test_lancerStrategie_succes(self):
        strat_mock = MagicMock()
        strat_mock.stop.return_value = False
        
        result = self.controler.lancerStrategie(strat_mock)
        
        self.assertTrue(result)
        self.assertEqual(self.controler.strat_en_cours, strat_mock)
        self.assertEqual(self.controler.strategie, 1)
        strat_mock.start.assert_called_once()

     def test_lancerStrategie_deja_occupe(self):
        strat_mock1 = MagicMock()
        strat_mock2 = MagicMock()
        self.controler.lancerStrategie(strat_mock1)
        
        result = self.controler.lancerStrategie(strat_mock2)
        
        self.assertFalse(result)
        strat_mock2.start.assert_not_called()
        
    @patch("controleur.sleep", return_value=None)  # Évite les pauses réelles
    def test_mainControleur_arret_strategie(self, _):
        strat_mock = MagicMock()
        strat_mock.stop.side_effect = [False, False, True]
        strat_mock.robA.setVitAngA = MagicMock()
        
        self.controler.strat_en_cours = strat_mock
        self.controler.strategie = 1
        self.controler.mainControleur()
        
        strat_mock.step.assert_called()
        strat_mock.robA.setVitAngA.assert_called_once_with(0)
        self.assertEqual(self.controler.strategie, 0)
        self.assertIsNone(self.controler.strat_en_cours)

if __name__ == "__main__":
    unittest.main()

