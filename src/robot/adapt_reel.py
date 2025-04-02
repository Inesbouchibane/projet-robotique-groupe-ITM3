from math import degrees
from .adapt import Adaptateur
from time import time

class Adaptateur_reel(Adaptateur):
    """Classe d'adaptation pour un robot réel simplifié"""

    def __init__(self, rob):
        """Constructeur prenant un robot en paramètre"""
        self.robot = rob
        self.robot.estCrash = False
        self.dist_parcourA = 0
        self.angle_parcourA = 0
        self.lastDist = self.robot.get_distance()
        self.lastRefresh = time()
        self.MOTOR_LEFT_RIGHT = 3  # Port combiné pour les deux moteurs

    def initialise(self):
        """Initialise les moteurs et réinitialise les compteurs"""
        self.robot.offset_motor_encoder(self.robot.MOTOR_LEFT, self.robot.get_motor_position()[0])
        self.robot.offset_motor_encoder(self.robot.MOTOR_RIGHT, self.robot.get_motor_position()[1])
        self.dist_parcourA = 0
        self.angle_parcourA = 0

    # --- Setters ---
    def setVitAngDA(self, dps):
        """Définit la vitesse angulaire de la roue droite"""
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, dps * 100)

    def setVitAngGA(self, dps):
        """Définit la vitesse angulaire de la roue gauche"""
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, dps * 100)

    def setVitAngA(self, dps):
        """Définit la vitesse angulaire pour les deux roues"""
        self.robot.set_motor_dps(self.MOTOR_LEFT_RIGHT, dps * 100)

    def setVitG(self, vit):
        """Définit la vitesse gauche (compatibilité)"""
        self.setVitAngGA(vit)

    def setVitD(self, vit):
        """Définit la vitesse droite (compatibilité)"""
        self.setVitAngDA(vit)

    # --- Getters ---
    def getDistanceObstacle(self):
        """Retourne la distance au capteur avec mise en cache"""
        tmps = time()
        if tmps - self.lastRefresh < 0.06:
            return self.lastDist
        self.lastDist = self.robot.get_distance()
        self.lastRefresh = tmps
        return self.lastDist

    def getDistanceParcourue(self):
        """Calcule la distance parcourue depuis la dernière mesure"""
        ang_g, ang_d = self.robot.get_motor_position()
        dist_g = (ang_g / 360) * self.robot.WHEEL_CIRCUMFERENCE
        dist_d = (ang_d / 360) * self.robot.WHEEL_CIRCUMFERENCE
        distance = (dist_g + dist_d) / 2
        self.dist_parcourA += distance
        return distance

    def getAngleParcouru(self):
        """Calcule l'angle parcouru"""
        ang_g, ang_d = self.robot.get_motor_position()
        dist_g = (ang_g / 360) * self.robot.WHEEL_CIRCUMFERENCE
        dist_d = (ang_d / 360) * self.robot.WHEEL_CIRCUMFERENCE
        angle = degrees((dist_d - dist_g) / self.robot.WHEEL_BASE_WIDTH)
        self.angle_parcourA += angle
        return angle

    def getVitG(self):
        """Retourne la vitesse angulaire gauche"""
        return self.robot.dpsg / 100  # Conversion en deg/s

    def getVitD(self):
        """Retourne la vitesse angulaire droite"""
        return self.robot.dpsd / 100  # Conversion en deg/s

    def getPosition(self):
        """Retourne une position simulée (pas de suivi précis ici)"""
        return (0, 0)  # Simplifié, pas de calcul précis

    def getDirection(self):
        """Retourne une direction simulée"""
        return [1, 0]  # Simplifié

    def isCrashed(self):
        """Vérifie si le robot est en collision"""
        return self.robot.estCrash

    # --- Méthodes non implémentées ou simplifiées ---
    def avancer(self, distance):
        """Simule l'avancement"""
        pass

    def tourner(self, angle):
        """Simule une rotation"""
        pass

    def arreter(self):
        """Arrête le robot"""
        self.robot.set_motor_dps(self.MOTOR_LEFT_RIGHT, 0)
