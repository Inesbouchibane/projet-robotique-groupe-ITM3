from logging import getLogger
from threading import Thread
from time import sleep
from utils import TIC_SIMULATION

class Controler:
    def __init__(self):
        self.logger = getLogger(self.__class__.__name__)
        self.strat_en_cours = None
        self.strategie = 0
        self.running = True
        Thread(target=self.mainControleur, daemon=True).start()

