from abc import ABC, abstractmethod
from logging import getLogger

class Adaptateur(ABC):
    """Interface commune pour tous les adaptateurs robotiques"""
    
    @abstractmethod
    def initialise(self):
        """Réinitialise les compteurs et états internes"""
        pass

    @abstractmethod
    def setVitAngGA(self, vit):
        """Définit la vitesse angulaire de la roue gauche (en degrés/s)"""
        pass

    @abstractmethod
    def setVitAngDA(self, vit):
        """Définit la vitesse angulaire de la roue droite (en degrés/s)"""
        pass

    @abstractmethod
    def getDistanceObstacle(self):
        """
        Retourne la distance à l'obstacle le plus proche en mm
        avec mise en cache pour optimisation
        """
        pass

    @abstractmethod
    def getDistanceParcourue(self):
        """Retourne la distance totale parcourue depuis l'initialisation (en mm)"""
        pass

    @abstractmethod
    def getAngleParcouru(self):
        """Retourne l'angle total parcouru depuis l'initialisation (en radians)"""
        pass

    @abstractmethod
    def getPosition(self):
        """Retourne la position actuelle sous forme de tuple (x, y) en mm"""
        pass

    @abstractmethod
    def getDirection(self):
        """Retourne le vecteur direction unitaire sous forme [x, y]"""
        pass

    @abstractmethod
    def isCrashed(self):
        """Retourne True si le robot est en état de collision"""
        pass

    @abstractmethod
    def arreter(self):
        """Arrête immédiatement tous les mouvements du robot"""
        pass
