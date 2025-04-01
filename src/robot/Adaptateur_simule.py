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

    def getVitG(self):
        return self.robot.get_VitG()
