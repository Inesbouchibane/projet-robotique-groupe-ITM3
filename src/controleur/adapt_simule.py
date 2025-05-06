from .adapt import Adaptateur
from src.robot.robot_simule import RobotSimule
from src.environnement import Environnement
from time import time
import math
import logging  # Ajout de l'importation

class AdaptateurSimule(Adaptateur):
    def __init__(self, robot: RobotSimule, environnement: Environnement):
        self.robot = robot
        self.environnement = environnement
        self.initialised = False
        self.last_refresh = time()
        self.last_dist = float('inf')
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Initialisation du robot")

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

    def tourne(self, gauche, droite):
        """Tourne en définissant les vitesses gauche et droite"""
        self.setVitAngG(gauche)
        self.setVitAngD(droite)

    def estCrash(self):
        """Retourne True si le robot est en collision avec un obstacle ou un mur."""
        if self.robot.estCrash:
            self.logger.debug("Collision détectée via robot.estCrash")
            return True

        # Calculer la boîte englobante du robot
        cos_a, sin_a = self.robot.direction
        half_length = self.robot.length / 2
        half_width = self.robot.width / 2
        # Coins de la boîte englobante
        corners = [
            (self.robot.x + cos_a * half_length + sin_a * half_width, self.robot.y + sin_a * half_length - cos_a * half_width),  # Avant-gauche
            (self.robot.x + cos_a * half_length - sin_a * half_width, self.robot.y + sin_a * half_length + cos_a * half_width),  # Avant-droit
            (self.robot.x - cos_a * half_length + sin_a * half_width, self.robot.y - sin_a * half_length - cos_a * half_width),  # Arrière-gauche
            (self.robot.x - cos_a * half_length - sin_a * half_width, self.robot.y - sin_a * half_length + cos_a * half_width),  # Arrière-droit
        ]

        # Vérifier les collisions avec les murs
        for x, y in corners:
            if x <= 0 or x >= self.environnement.largeur or y <= 0 or y >= self.environnement.longueur:
                self.robot.estCrash = True
                self.logger.debug(f"Collision avec mur détectée à ({x:.2f}, {y:.2f})")
                return True

        # Vérifier les collisions avec les obstacles
        for obs in self.environnement.listeObs:
            for px, py in obs.points:
                for x, y in corners:
                    dist = math.sqrt((px - x)**2 + (py - y)**2)
                    if dist < 10:  # Seuil augmenté à 10 mm pour plus de fiabilité
                        self.robot.estCrash = True
                        self.logger.debug(f"Collision avec obstacle détectée à ({x:.2f}, {y:.2f}) près de ({px:.2f}, {py:.2f})")
                        return True

        return False
 
    def getDistanceParcourue(self):
        return self.robot.getDistanceParcouru()

    def getAngleParcouru(self):
        return self.robot.getAngleParcouru()

    def getPosition(self):
        return (self.robot.x, self.robot.y)

    def getDirection(self):
        return self.robot.direction

    def get_imageA(self):
        """Simule la capture d'une image et détecte la position de la balise dans l'image."""
        self.logger.debug("Capture d'image simulée pour détecter la balise")
        
        # Vérifier si la balise existe dans l'environnement
        if not hasattr(self.environnement, 'beacon_position'):
            self.logger.debug("Aucune balise présente dans l'environnement")
            return None

        # Position de la balise
        beacon_x, beacon_y = self.environnement.beacon_position
        robot_x, robot_y = self.robot.x, self.robot.y
        cos_a, sin_a = self.robot.direction

        # Calculer la position relative de la balise par rapport au robot
        rel_x = beacon_x - robot_x
        rel_y = beacon_y - robot_y

        # Distance entre le robot et la balise
        distance = math.sqrt(rel_x**2 + rel_y**2)

        # Calculer l'angle entre la direction du robot et la balise
        dot_product = rel_x * cos_a + rel_y * sin_a
        if distance == 0:
            return None
        angle_to_beacon = math.acos(dot_product / distance)
        cross_product = rel_x * sin_a - rel_y * cos_a
        if cross_product < 0:
            angle_to_beacon = -angle_to_beacon

        # Simuler un champ de vision de la caméra (par exemple, 90 degrés)
        fov = math.radians(90)
        if abs(angle_to_beacon) > fov / 2:
            self.logger.debug("Balise hors du champ de vision")
            return None

        # Simuler une image de 640x480 pixels
        image_width, image_height = 640, 480

        # Mapper l'angle à une position horizontale dans l'image
        center_x = (angle_to_beacon / (fov / 2)) * (image_width / 2) + (image_width / 2)
        center_y = image_height / 2  # On suppose que la balise est à la même hauteur

        # Vérifier si la balise est dans l'image
        if 0 <= center_x <= image_width:
            self.logger.debug(f"Balise détectée à la position ({center_x:.2f}, {center_y:.2f}) dans l'image")
            return (center_x, center_y, image_width, image_height)
        else:
            self.logger.debug("Balise hors de l'image")
            return None

    def getVitG(self):
        return self.robot.get_VitG()

    def getVitD(self):
        return self.robot.get_VitD()

    def isCrashed(self):
        return self.robot.estCrash or self.getDistanceObstacle() < 5

    def arreter(self):
        """Implémentation de la méthode arreter"""
        self.robot.arreter()
