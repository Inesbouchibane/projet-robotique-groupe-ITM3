from .adapt import Adaptateur
from .robot_simule import RobotSimule
from src.environnement import Environnement
from time import time
import math

class AdaptateurSimule(Adaptateur):
    def __init__(self, robot: RobotSimule, environnement: Environnement):
        self.robot = robot
        self.environnement = environnement
        self.initialised = False
        self.last_refresh = time()
        self.last_dist = float('inf')

    def initialise(self):
        self.robot.arreter()
        self.robot.reset_tracking()
        self.initialised = True
        self.last_refresh = time()

    def setVitAngA(self, vit):
        self.robot.set_VitG(vit)
        self.robot.set_VitD(vit)

    def setVitAngGA(self, vit):
        self.robot.set_VitG(vit)

    def setVitAngDA(self, vit):
        self.robot.set_VitD(vit)

    def setVitG(self, vit):
        self.robot.set_VitG(vit)

    def setVitD(self, vit):
        self.robot.set_VitD(vit)

    def getDistanceObstacle(self):
        current_time = time()
        if current_time - self.last_refresh < 0.06:
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
        return self.last_dist


    def getVitD(self):
        return self.robot.get_VitD()

    def getVitG(self):
        return self.robot.get_VitG()

    def getDistanceParcourue(self):
        return self.robot.getDistanceParcouru()

    def getAngleParcouru(self):
        return self.robot.getAngleParcouru()

    def getPosition(self):
        return (self.robot.x, self.robot.y)

    def getDirection(self):
        return self.robot.direction

    def isCrashed(self):
        return self.robot.estCrash or self.getDistanceA() < 5
    
    def arreter(self):
        """Implémentation de la méthode arreter"""
        self.robot.arreter()
        self.robot.estCrash = True 
