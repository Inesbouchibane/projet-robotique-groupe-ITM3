from threading import Thread
from time import sleep
from logging import getLogger
from src.utils import TIC_CONTROLEUR
from .strategies import setStrategieCarre, StrategieAuto, StrategieAvancer

class Controler:
    def __init__(self, adaptateur=None):
        self.logger = getLogger(self.__class__.__name__)
        self.strategie = None
        self.running = False
        self.adaptateur = adaptateur
        
    def set_strategie(self, strategie_type, **kwargs):
        if isinstance(strategie_type, str):
            if strategie_type == "tracer_carre":
                self.strategie = setStrategieCarre(kwargs.get('longueur_cote', 100))
            elif strategie_type == "auto":
                self.strategie = StrategieAuto(kwargs.get('vitAngG', 0), kwargs.get('vitAngD', 0))
            elif strategie_type == "avancer":
                self.strategie = StrategieAvancer(kwargs.get('distance', 100))
            elif strategie_type == "arret_mur":
                self.strategie = setStrategieArretMur(self.adaptateur, kwargs.get('distarret', 50))
        else:
            self.strategie = strategie_type(**kwargs) if isinstance(strategie_type, type) else strategie_type
        self.logger.info(f"Stratégie définie : {self.strategie.__class__.__name__}")

    def lancerStrategie(self, strategie=None):
        if strategie:
            self.strategie = strategie
        self.running = True
        if self.strategie is not None and self.adaptateur is not None:
            self.logger.info(f"Lancement du thread pour {self.strategie.__class__.__name__}")
            Thread(target=self.run_strategie, daemon=True).start()
        else:
            self.logger.error("Erreur : stratégie ou adaptateur non défini")

    def run_strategie(self):
        if self.strategie is not None:
            self.logger.info(f"Exécution de {self.strategie.__class__.__name__}")
            self.strategie.start(self.adaptateur)
            while self.running and not self.strategie.stop(self.adaptateur):
                self.strategie.step(self.adaptateur)
                sleep(TIC_CONTROLEUR)
            self.running = False
            self.adaptateur.arreter()
            self.logger.info(f"Fin de {self.strategie.__class__.__name__}")
        else:
            self.logger.error("Aucune stratégie à exécuter")

    def stop(self):
        self.running = False
        self.logger.info("Arrêt manuel du contrôleur")