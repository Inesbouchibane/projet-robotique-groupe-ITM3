from abc import ABC, abstractmethod

class Adaptateur(ABC):
    @abstractmethod
    def initialise(self):
        pass

    @abstractmethod
    def setVitAngA(self, vit):
        pass

    @abstractmethod
    def setVitG(self, vit):
        pass

    @abstractmethod
    def setVitD(self, vit):
        pass

    @abstractmethod
    def getDistanceObstacle(self):
        pass

    @abstractmethod
    def getVitD(self):
        pass

    @abstractmethod
    def getVitG(self):
        pass

    @abstractmethod
    def getDistanceParcourue(self):
        pass

    @abstractmethod
    def getAngleParcouru(self):
        pass

    @abstractmethod
    def getPosition(self):
        """Retourne la position actuelle (x, y) du robot"""
        pass

    @abstractmethod
    def getDirection(self):
        """Retourne le vecteur direction du robot"""
        pass

    @abstractmethod
    def isCrashed(self):
        """Retourne si le robot est en collision"""
        pass

    @abstractmethod
    def setVitAngGA(self, vit):
        pass

    @abstractmethod
    def setVitAngDA(self, vit):
        pass

    @abstractmethod
    def getDistanceA(self):
        pass
