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
getDistanceParcourue
    def setVitAngGA(self, vit):
        self.robot.vitAngG = vit

    def setVitAngA(self, vit):
        self.robot.setVitAng(vit)

    def getDistanceA(self):
        return self.robot.getDistance(self.env)
    def getDistanceParcourue(self):
        pos_actuelle = (self.robot.x, self.robot.y)
        dist = getDistanceFromPts(pos_actuelle, self.last_point)
        self.last_point = pos_actuelle
        return dist

    def getAngleParcouru(self):
        dir_actuelle = self.robot.direction
        angle = getAngleFromVect(self.last_dir, dir_actuelle)
        self.last_dir = dir_actuelle
        return angle
