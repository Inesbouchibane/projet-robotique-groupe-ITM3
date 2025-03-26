from logging import getLogger
from threading import Thread
from time import sleep
from utils import TIC_SIMULATION

class Controler:
    """Classe permettant de gérer l'exécution des stratégies du robot."""

    def __init__(self):
        """Initialisation du contrôleur."""
        self.logger = getLogger(self.__class__.__name__)
        self.strat_en_cours = None
        self.strategie = False  # Indique si une stratégie est active
        self.running = True
        Thread(target=self.mainControleur, daemon=True).start()

    def mainControleur(self):
        """Boucle principale exécutant la stratégie active."""
        while self.running:
            if self.strategie and self.strat_en_cours:
                self.logger.debug("Contrôleur actif, exécution d'un step.")
                if not self.strat_en_cours.stop():
                    self.strat_en_cours.step()
                else:
                    self.logger.debug("Stratégie terminée, arrêt du contrôleur.")
                    self.strategie = False
                    self.strat_en_cours.robA.setVitAngA(0)
                    self.strat_en_cours = None
            sleep(TIC_SIMULATION)

    def lancerStrategie(self, strat):
        """Lance une nouvelle stratégie si aucune n'est en cours."""
        if self.strategie:
            self.logger.error("Impossible de lancer une nouvelle stratégie : contrôleur occupé.")
            return False
        self.strat_en_cours = strat
        self.strategie = True
        self.strat_en_cours.start()
        self.logger.debug("Nouvelle stratégie lancée.")
        return True

