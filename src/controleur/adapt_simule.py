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

    def setVitAngGA(self, vit):
        self.robot.set_VitG(vit)
        self.logger.info("setVitAngG = %d", vit)

    def setVitAngDA(self, vit):
        self.robot.set_VitD(vit)
        self.logger.info("setVitAngD = %d", vit)

    def setVitG(self, vit):
        self.robot.set_VitG(vit)

    def setVitD(self, vit):
        self.robot.set_VitD(vit)

    def tourne(self, gauche, droite):
        """Tourne en définissant les vitesses gauche et droite"""
        self.setVitAngGA(gauche)
        self.setVitAngDA(droite)

    def getDistanceObstacle(self):
        current_time = time()
        if current_time - self.last_refresh < 0.06:
            self.logger.debug("capteurDistance - Cache utilisé")
            return self.last_dist
        lstPoints = [
            (self.robot.x - self.robot.width/2, self.robot.y + self.robot.length/2),
            (self.robot.x + self.robot.width/2, self.robot.y + self.robot.length/2),
            (self.robot.x + self.robot.width/2, self.robot.y - self.robot.length/2),
            (self.robot.x - self.robot.width/2, self.robot.y - self.robot.length/2)
        ]
        min_dist = float('inf')
        for x, y in lstPoints:
            for obs in self.environnement.listeObs:
                for px, py in obs.points:
                    dist = math.sqrt((x - px)**2 + (y - py)**2)
                    min_dist = min(min_dist, dist)
        self.last_dist = min_dist if min_dist != float('inf') else 1000
        self.last_refresh = current_time
        self.logger.debug("capteurDistance")
        return self.last_dist

    def getDistanceParcourue(self):
        return self.robot.getDistanceParcouru()

    def getAngleParcouru(self):
        return self.robot.getAngleParcouru()

    def getPosition(self):
        return (self.robot.x, self.robot.y)

    def getDirection(self):
        return self.robot.direction

    def get_imageA(self):
        """Retourne une image simulée (mock pour compatibilité)"""
        self.logger.debug("Capture d'image simulée")
        return bytearray([0] * 640 * 480 * 3)  # Image noire 640x480 RGB

    def getVitG(self):
        return self.robot.get_VitG()

    def getVitD(self):
        return self.robot.get_VitD()

    def isCrashed(self):
        return self.robot.estCrash or self.getDistanceObstacle() < 5

    def arreter(self):
        """Implémentation de la méthode arreter"""
        self.robot.arreter()
   
    #correction : implementation de dessine dans l'adaptateur pr les strategies et non dans le robot
    def dessine (self,b) : 
        return self.robot.crayon = b   
