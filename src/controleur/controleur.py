from threading import Thread
from time import sleep
from logging import getLogger
from src.utils import TIC_CONTROLEUR
from .strategies import setStrategieCarre, StrategieAuto, StrategieAvancer, StrategieArretMur, StrategieSuivreBalise, StrategieClavier

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
                adaptateur = kwargs.get('adaptateur', self.adaptateur)
                distance_arret = kwargs.get('distance_arret', 5)
                self.logger.debug(f"Arguments pour arret_mur : adaptateur={adaptateur}, distance_arret={distance_arret}")
                self.strategie = StrategieArretMur(adaptateur, distance_arret)
            elif strategie_type == "suivre_balise":
                adaptateur = kwargs.get('adaptateur', self.adaptateur)
                self.strategie = StrategieSuivreBalise(adaptateur)
            elif strategie_type == "clavier":
                adaptateur = kwargs.get('adaptateur', self.adaptateur)
                key_map = kwargs.get('key_map', {})
                self.logger.debug(f"Arguments pour clavier : adaptateur={adaptateur}, key_map={key_map}")
                self.strategie = StrategieClavier(adaptateur, key_map)
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