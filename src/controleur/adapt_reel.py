from math import degrees
from .adapt import Adaptateur
from src.robot.robot_mockup import MockupRobot
from time import time
import logging

class Adaptateur_reel(Adaptateur):
    """
Classe Adaptateur_reel :
Ce module permet de faire l’interface entre un robot réel (simplifié ici avec MockupRobot)
et les commandes haut niveau (comme vitesse ou acquisition d’image).
"""

    def __init__(self, rob):
        """
Initialise l'adaptateur avec un robot réel ou simulé (Mockup).
Initialise les compteurs de distance/angle et récupère la distance initiale.
"""
        self.robot = rob
        self.dist_parcourA = 0
        self.angle_parcourA = 0
        self.lastDist = self.robot.get_distance()
        self.lastRefresh = time()
        self.MOTOR_LEFT_RIGHT = 3  # Port combiné pour les deux moteurs
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Initialisation du robot")

    def initialise(self):
        """
Réinitialise les encodeurs moteurs gauche et droit,
et remet les compteurs de distance et d'angle à zéro.
"""
        self.robot.offset_motor_encoder(self.robot.MOTOR_LEFT, self.robot.get_motor_position()[0])
        self.robot.offset_motor_encoder(self.robot.MOTOR_RIGHT, self.robot.get_motor_position()[1])
        self.dist_parcourA = 0
        self.angle_parcourA = 0

    # --- Setters ---
    def setVitAngDA(self, dps):
        """
Applique une vitesse angulaire donnée (en dps) à la roue droite.
Le facteur 100 est une convention interne du robot.
"""
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, dps * 100)
        self.logger.info("setVitAngD = %d", dps)

    def setVitAngGA(self, dps):
        """
Applique une vitesse angulaire donnée (en dps) à la roue gauche.
Le facteur 100 est une convention interne du robot.
"""
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, dps * 100)
        self.logger.info("setVitAngG = %d", dps)

    def setVitAngA(self, dps):
        """
Applique une vitesse égale aux deux roues (gauche et droite).
Utilisé pour faire avancer/reculer droit.
"""
        self.robot.set_motor_dps(self.MOTOR_LEFT_RIGHT, dps * 100)
        self.logger.info("setVitAng = %d", dps)


    def tourne(self, gauche, droite):
        """
Commande de mouvement différentielle :
permet de tourner le robot en fixant la vitesse des deux roues.
"""
        self.setVitAngGA(gauche)
        self.setVitAngDA(droite)

    # --- Getters ---

    def getDistanceParcourue(self):
        """
Calcule la distance moyenne parcourue par les deux roues depuis le début,
et la cumule dans une variable globale.
"""
        ang_g, ang_d = self.robot.get_motor_position()
        dist_g = (ang_g / 360) * self.robot.WHEEL_CIRCUMFERENCE
        dist_d = (ang_d / 360) * self.robot.WHEEL_CIRCUMFERENCE
        distance = (dist_g + dist_d) / 2
        self.dist_parcourA += distance
        return self.dist_parcourA  # Retourne la distance totale

    def getAngleParcouru(self):
        """
Calcule la différence de distance entre les deux roues,
convertie en angle à partir de l'écartement des roues (base).
"""
        ang_g, ang_d = self.robot.get_motor_position()
        dist_g = (ang_g / 360) * self.robot.WHEEL_CIRCUMFERENCE
        dist_d = (ang_d / 360) * self.robot.WHEEL_CIRCUMFERENCE
        angle = degrees((dist_d - dist_g) / self.robot.WHEEL_BASE_WIDTH)
        self.angle_parcourA += angle
        return self.angle_parcourA  # Retourne l'angle total

    def get_imageA(self):
        """
Capture une image via le robot (caméra ou équivalent mock).
"""
        return self.robot.get_image()

    def getVitG(self):
        """
Renvoie la dernière vitesse appliquée à la roue gauche (en deg/s).
"""
        return self.robot.dpsg / 100  # Conversion en deg/s

    def getVitD(self):
        """
Renvoie la dernière vitesse appliquée à la roue droite (en deg/s).
"""
        return self.robot.dpsd / 100  # Conversion en deg/s

    def arreter(self):
        """
Envoie une commande nulle aux moteurs pour arrêter tout mouvement.
"""
        self.robot.set_motor_dps(self.MOTOR_LEFT_RIGHT, 0)

    def getDistanceObstacle(self):
        """
        Retourne une distance simulée à un obstacle (valeur fixe).
        Cette méthode est requise par les stratégies de déplacement.
        """
        return 150
    