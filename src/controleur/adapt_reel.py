# adapt_reel.py
import cv2
import numpy as np
from math import degrees
from .adapt import Adaptateur
from src.robot.robot_mockup import MockupRobot
from time import time
import logging

class Adaptateur_reel(Adaptateur):
    def __init__(self, rob):
        self.robot = rob
        self.dist_parcourA = 0
        self.angle_parcourA = 0
        self.MOTOR_LEFT_RIGHT = self.robot.MOTOR_LEFT + self.robot.MOTOR_RIGHT
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Initialisation du robot")
        self.lastRefresh = time()
        self.lastDist = self.robot.get_distance()

    def initialise(self):
        self.robot.offset_motor_encoder(self.robot.MOTOR_LEFT, self.robot.get_motor_position()[0])
        self.robot.offset_motor_encoder(self.robot.MOTOR_RIGHT, self.robot.get_motor_position()[1])
        self.dist_parcourA = 0
        self.angle_parcourA = 0

    def setVitAngD(self, dps):
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, dps * 100)
        self.logger.info("setVitAngD = %d", dps)

    def setVitAngG(self, dps):
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, dps * 100)
        self.logger.info("setVitAngG = %d", dps)

    def setVitAngA(self, dps):
        self.robot.set_motor_dps(self.MOTOR_LEFT_RIGHT, dps * 100)
        self.logger.info("setVitAng = %d", dps)

    def tourne(self, gauche, droite):
        self.setVitAngG(gauche)
        self.setVitAngD(droite)

    def getDistanceParcourue(self):
        ang_g, ang_d = self.robot.get_motor_position()
        dist_g = (ang_g / 360) * self.robot.WHEEL_CIRCUMFERENCE
        dist_d = (ang_d / 360) * self.robot.WHEEL_CIRCUMFERENCE
        distance = (dist_g + dist_d) / 2
        self.dist_parcourA += distance
        return self.dist_parcourA

    def getAngleParcouru(self):
        ang_g, ang_d = self.robot.get_motor_position()
        dist_g = (ang_g / 360) * self.robot.WHEEL_CIRCUMFERENCE
        dist_d = (ang_d / 360) * self.robot.WHEEL_CIRCUMFERENCE
        angle = degrees((dist_d - dist_g) / self.robot.WHEEL_BASE_WIDTH)
        self.angle_parcourA += angle
        return self.angle_parcourA

    def estCrash(self):
        """Retourne True si le robot est en collision (basé sur l'état interne)."""
        return getattr(self.robot, 'estCrash', False)  # Default to False if estCrash not defined

    def get_imageA(self):
        """
        Capture une image via le robot et retourne un tableau NumPy.
        Si aucune image n'est disponible, retourne une image noire simulée.
        """
        image = self.robot.get_image()
        if image is None:
            self.logger.debug("Aucune image reçue, simulation d'une image noire")
            image = np.zeros((480, 640, 3), dtype=np.uint8)  # 640x480 RGB, black
            # Optional: Simulate a red balise (100x100 pixels) at the center
            image[190:290, 270:370, :] = [0, 0, 255]  # BGR: Red
        return image
    
    def getDistanceA(self):
        """Getter qui renvoie la distance mesurée par le capteur de distance"""
        tmps = time()
        if (tmps - self.lastRefresh < 0.06):
            return self.lastDist
        
        self.lastDist = self.robot.get_distance()
        self.lastRefresh = tmps
        return self.lastDist

    def getVitG(self):
        return self.robot.dpsg / 100

    def getVitD(self):
        return self.robot.dpsd / 100

    def arreter(self):
        self.robot.set_motor_dps(self.MOTOR_LEFT_RIGHT, 0)

    def cleanup(self):
        """
        Nettoie les ressources, arrête les moteurs et libère la caméra si nécessaire.
        """
        self.arreter()
        self.logger.info("Cleanup effectué")

    def adjust_position(self, target_distance):
        """Correction physique progressive pour le robot réel"""
        current = self.getDistanceParcourue()
        error = target_distance - current
        tolerance = 5  # mm de tolérance
        
        if abs(error) > tolerance:
            correction_speed = VIT_ANG_AVAN * (0.5 if error > 0 else -0.5)
            self.setVitAngA(correction_speed)
            sleep(0.2 * abs(error)/100)  # Durée proportionnelle à l'erreur
            self.arreter()
            self.logger.info(f"Position ajustée: {error:.1f}mm corrigés")

    def adjust_angle(self, target_angle_rad):
        """Correction d'angle par petites rotations"""
        current_rad = math.radians(self.getAngleParcouru())
        error_rad = target_angle_rad - current_rad
        tolerance = math.radians(0.5)  # 0.5° de tolérance
        
        if abs(error_rad) > tolerance:
            correction_speed = VIT_ANG_TOUR * (0.5 if error_rad > 0 else -0.5)
            self.tourne(-correction_speed, correction_speed)
            sleep(0.1 * abs(error_rad)/math.radians(10))  # Durée proportionnelle
            self.arreter()
            self.logger.info(f"Angle ajusté: {math.degrees(error_rad):.1f}° corrigés")