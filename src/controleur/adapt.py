from abc import ABC, abstractmethod
import logging

class Adaptateur(ABC):
    """Interface commune pour tous les adaptateurs robotiques"""

    @abstractmethod
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Initialisation du robot")

    @abstractmethod
    def initialise(self):
        """Réinitialise les compteurs et états internes"""
        pass

    @abstractmethod
    def setVitAngD(self, dps):
        """Définit la vitesse angulaire de la roue droite (en degrés/s)"""
        pass

    @abstractmethod
    def setVitAngG(self, dps):
        """Définit la vitesse angulaire de la roue gauche (en degrés/s)"""
        pass

    @abstractmethod
    def setVitAngA(self, dps):
        """Définit la vitesse angulaire pour les deux roues (en degrés/s)"""
        pass

    @abstractmethod
    def tourne(self, gauche, droite):
        """Tourne en définissant les vitesses gauche et droite"""
        pass

    @abstractmethod
    def getDistanceParcourue(self):
        """Retourne la distance totale parcourue depuis l'initialisation (en mm)"""
        pass

    @abstractmethod
    def getAngleParcouru(self):
        """Retourne l'angle total parcouru depuis l'initialisation (en degrés)"""
        pass

    @abstractmethod
    def get_imageA(self):
        """Retourne une image capturée par le robot"""
        pass

    @abstractmethod
    def arreter(self):
        """Arrête immédiatement tous les mouvements du robot"""
        pass

    @abstractmethod
    def adjust_position(self, target_distance):
        """Corrige la position pour atteindre exactement la distance cible"""
        pass

    @abstractmethod
    def adjust_angle(self, target_angle):
        """Corrige l'angle pour atteindre exactement l'angle cible (en radians)"""
        pass