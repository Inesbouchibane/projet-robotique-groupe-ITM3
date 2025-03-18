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

    def mainControleur(self):
        while self.running:
            if self.strategie:
                self.logger.debug("Controller active, calling step")
                if not self.strat_en_cours.stop():
                    self.strat_en_cours.step()
                else:
                    self.logger.debug("Strategy completed, stopping")
                    self.strategie = 0
                    self.strat_en_cours.robA.setVitAngA(0)
                    self.strat_en_cours = None
            sleep(TIC_SIMULATION)
    def lancerStrategie(self, strat):
        if self.strategie:
            self.logger.error("Contrôleur occupé")
            return False
        self.strat_en_cours = strat
        self.strategie = 1
        self.strat_en_cours.start()
        self.logger.debug("Strategy launched")
        return True