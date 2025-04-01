from abc import ABC, abstractmethod

class Robot(ABC):
    @abstractmethod
    def avancer(self, valeur):
        """Fait avancer le robot de valeur"""
        pass

    @abstractmethod
    def arreter(self):
        """Arrete le robot"""
        pass

    @abstractmethod
    def set_VitG(self, valeur):
        """Donne une vitesse à la roue gauche"""
        pass

    @abstractmethod
    def set_VitD(self, valeur):
        """Donne une vitesse à la roue droite"""
        pass

    @abstractmethod
    def getDistanceParcouru(self):
        """Donne la distance parcourue par le robot"""
        pass

    @abstractmethod
    def getDistanceObstacle(self):
        """Retourne la distance du robot à l'obstacle devant lui"""
        pass

    @abstractmethod
    def get_VitG(self):
        """Retourne la vitesse de la roue gauche"""
        pass

    @abstractmethod
    def get_VitD(self):
        """Retourne la vitesse de la roue droite"""
        pass

    @abstractmethod
    def refresh(self, delta_t=None):
        """Met à jour l'état du robot"""
        pass

    @abstractmethod
    def getAngleParcouru(self):
        """Retourne l'angle parcouru lors de la rotation en radians"""
        pass

    @abstractmethod
    def getDistanceRoues(self):
        """Retourne la distance entre les deux roues"""
        pass
