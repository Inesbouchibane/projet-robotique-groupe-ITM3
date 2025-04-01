from .adapt import Adaptateur
from utils import getAngleFromVect, getDistanceFromPts

class Adaptateur_simule(Adaptateur):
    """Adaptateur pour simuler un robot dans un environnement virtuel."""
    def __init__(self, robot, env):
        self.robot = robot
        self.env = env
        self.last_point = (robot.x, robot.y)
        self.last_dir = robot.direction

    def initialise(self):
        self.last_point = (self.robot.x, self.robot.y)
        self.last_dir = self.robot.direction

    def setVitAngDA(self, vit):
        self.robot.vitAngD = vit

    def setVitAngGA(self, vit):
        self.robot.vitAngG = vit

    def setVitAngA(self, vit):
        self.robot.setVitAng(vit)
        
    def getVitD(self):
        return self.robot.get_VitD()
        
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


    def getVitG(self):
        return self.robot.get_VitG()

   def getDistanceParcourue(self):
        return self.robot.getDistanceParcouru()

    def getAngleParcouru(self):
        return self.robot.getAngleParcouru()
