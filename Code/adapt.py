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
