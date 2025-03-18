import unittest
from unittest.mock import MagicMock, patch
from controleur import Controler
from time import sleep
from utils import TIC_SIMULATION

class TestControler(unittest.TestCase):
    def setUp(self):
        self.controler = Controler()
        self.controler.running = False  # Empêcher le thread de tourner en test

