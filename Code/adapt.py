from utils import getAngleFromVect, getDistanceFromPts

class Adaptateur:
    def initialise(self): pass
    def setVitAngA(self, vit): pass
    def getDistanceA(self): pass
    def getDistanceParcourue(self): pass
    def getAngleParcouru(self): pass
    
class Adaptateur_simule(Adaptateur):
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

    def getDistanceA(self):
        return self.robot.getDistance(self.env)
