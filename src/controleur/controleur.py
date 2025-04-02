from threading import Thread
from time import sleep
from logging import getLogger
from src.utils import TIC_CONTROLEUR
from .strategies import setStrategieCarre, StrategieAuto

class Controler:
    def __init__(self, adaptateur=None):
        self.logger = getLogger(self.__class__.__name__)
        self.strategie = None
        self.running = False
        self.adaptateur = adaptateur
        
    def set_strategie(self, strategie_type, **kwargs):
        if strategie_type == "tracer_carre":
            self.strategie = setStrategieCarre(kwargs.get('longueur_cote', 100))
        elif strategie_type == "auto":
            self.strategie = StrategieAuto(kwargs.get('vitAngG', 0), kwargs.get('vitAngD', 0))

    def lancerStrategie(self, strategie=None):
        if strategie:
            self.strategie = strategie
        self.running = True
        if self.strategie is not None and self.adaptateur is not None:
            Thread(target=self.run_strategie, daemon=True).start()

    def run_strategie(self):
        if self.strategie is not None:
            self.strategie.start(self.adaptateur)
            while self.running and not self.strategie.stop(self.adaptateur):
                self.strategie.step(self.adaptateur)
                sleep(TIC_CONTROLEUR)
            self.running = False
            self.logger.debug("Stratégie terminée.")

    def stop(self):
        self.running = False
