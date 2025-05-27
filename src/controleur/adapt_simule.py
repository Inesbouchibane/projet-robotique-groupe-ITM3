from src.controleur.adapt import Adaptateur
from src.robot.robot_simule import RobotSimule
from src.environnement import Environnement
from time import time
import math
import numpy as np
from src.utils import getDistanceFromPts
import logging

class AdaptateurSimule(Adaptateur):
    def __init__(self, robot: RobotSimule, environnement: Environnement):
        self.robot = robot
        self.environnement = environnement
        self.initialised = False
        self.last_refresh = time()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.robot.set_environnement(environnement)

    def initialise(self):
        self.robot.arreter()
        self.robot.reset_tracking()
        self.initialised = True
        self.last_refresh = time()

    def setVitAngA(self, vit):
        self.robot.set_VitG(vit)
        self.robot.set_VitD(vit)
        self.logger.info("setVitAng = %d", vit)

    def setVitAngG(self, vit):
        self.robot.set_VitG(vit)
        self.logger.info("setVitAngG = %d", vit)

    def setVitAngD(self, vit):
        self.robot.set_VitD(vit)
        self.logger.info("setVitAngD = %d", vit)

    def setVitG(self, vit):
        self.robot.set_VitG(vit)

    def setVitD(self, vit):
        self.robot.set_VitD(vit)

    def tourne(self, gauche, droite):
        self.setVitAngG(gauche)
        self.setVitAngD(droite)

    def estCrash(self):
        if self.robot.estCrash:
            self.logger.debug("Collision détectée via robot.estCrash")
            return True
        cos_a, sin_a = self.robot.direction
        half_length = self.robot.length / 2
        half_width = self.robot.width / 2
        corners = [
            (self.robot.x + cos_a * half_length + sin_a * half_width, self.robot.y + sin_a * half_length - cos_a * half_width),
            (self.robot.x + cos_a * half_length - sin_a * half_width, self.robot.y + sin_a * half_length + cos_a * half_width),
            (self.robot.x - cos_a * half_length + sin_a * half_width, self.robot.y - sin_a * half_length - cos_a * half_width),
            (self.robot.x - cos_a * half_length - sin_a * half_width, self.robot.y - sin_a * half_length + cos_a * half_width),
        ]
        # Check for wall collisions
        for x, y in corners:
            if x <= 0 or x >= self.environnement.largeur or y <= 0 or y >= self.environnement.longueur:
                self.robot.estCrash = True
                self.logger.debug(f"Collision avec mur détectée à ({x:.2f}, {y:.2f})")
                return True
        # Check for obstacle collisions with increased tolerance
        tolerance = max(self.robot.width, self.robot.length) / 2  # Use robot's size for tolerance
        for obs in self.environnement.listeObs:
            points = obs.points
            num_points = len(points)
            for i in range(num_points):
                p1 = points[i]
                p2 = points[(i + 1) % num_points]  # Connect points to form edges
                for x, y in corners:
                    dist = self._point_to_segment_distance((x, y), p1, p2)
                    self.logger.debug(f"Distance coin à segment ({p1}, {p2}) : {dist:.2f}mm")
                    if dist < tolerance:
                        self.robot.estCrash = True
                        self.logger.debug(f"Collision avec obstacle détectée à ({x:.2f}, {y:.2f}) près de segment ({p1}, {p2})")
                        return True
        return False

    def _point_to_segment_distance(self, p, p1, p2):
        """Calculate the shortest distance from point p to the line segment p1-p2."""
        px, py = p
        x1, y1 = p1
        x2, y2 = p2
        # Vector from p1 to p2
        dx, dy = x2 - x1, y2 - y1
        length_sq = dx**2 + dy**2
        if length_sq == 0:
            return getDistanceFromPts(p, p1)
        # Projection parameter
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / length_sq))
        # Projection point
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        return getDistanceFromPts(p, (proj_x, proj_y))

    def getDistanceParcourue(self):
        return self.robot.getDistanceParcouru()

    def getAngleParcouru(self):
        return self.robot.getAngleParcouru()

    def getPosition(self):
        return (self.robot.x, self.robot.y)

    def getDirection(self):
        return self.robot.direction

    def get_imageA(self):
        if not hasattr(self.environnement, 'beacon_position') or self.environnement.beacon_position is None:
            self.logger.debug("Aucune balise présente")
            return np.zeros((480, 640, 3), dtype=np.uint8)
        beacon_x, beacon_y = self.environnement.beacon_position
        robot_x, robot_y = self.robot.x, self.robot.y
        cos_a, sin_a = self.robot.direction
        rel_x = beacon_x - robot_x
        rel_y = beacon_y - robot_y
        distance = math.sqrt(rel_x**2 + rel_y**2)
        if distance == 0:
            return np.zeros((480, 640, 3), dtype=np.uint8)
        dot_product = rel_x * cos_a + rel_y * sin_a
        angle_to_beacon = math.acos(dot_product / distance)
        cross_product = rel_x * sin_a - rel_y * cos_a
        if cross_product < 0:
            angle_to_beacon = -angle_to_beacon
        fov = math.radians(90)
        if abs(angle_to_beacon) > fov / 2:
            self.logger.debug("Balise hors du champ de vision")
            return np.zeros((480, 640, 3), dtype=np.uint8)
        image_width, image_height = 640, 480
        center_x = (angle_to_beacon / (fov / 2)) * (image_width / 2) + (image_width / 2)
        center_y = image_height / 2
        if not (0 <= center_x <= image_width):
            self.logger.debug("Balise hors de l'image")
            return np.zeros((480, 640, 3), dtype=np.uint8)
        image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
        x_min = int(max(0, center_x - 50))
        x_max = int(min(image_width, center_x + 50))
        y_min = int(max(0, center_y - 50))
        y_max = int(min(image_height, center_y + 50))
        if x_max > x_min and y_max > y_min:
            mid_x = (x_min + x_max) // 2
            mid_y = (y_min + y_max) // 2
            image[y_min:mid_y, x_min:mid_x] = [0, 0, 255]  # Rouge
            image[y_min:mid_y, mid_x:x_max] = [255, 0, 0]   # Bleu
            image[mid_y:y_max, x_min:mid_x] = [0, 255, 0]   # Vert
            image[mid_y:y_max, mid_x:x_max] = [0, 255, 255] # Jaune
        self.logger.debug(f"Image simulée avec balise à ({center_x:.2f}, {center_y:.2f})")
        return image

    def getVitG(self):
        return self.robot.get_VitG()

    def getVitD(self):
        return self.robot.get_VitD()

    def getDistanceA(self):
        return self.robot.getDistanceObstacle()

    def arreter(self):
        self.robot.arreter()

    def step(self, delta_t):
        if self.estCrash():
            self.arreter()
            return
        self.robot.refresh(delta_t)
        self.last_refresh = time()

    def adjust_position(self, target_distance):
        self.robot.adjust_position(target_distance)

    def adjust_angle(self, target_angle):
        self.robot.adjust_angle(target_angle)