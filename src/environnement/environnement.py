from src.utils import getDistanceFromPts, TIC_SIMULATION
from .obstacle import Obstacle

class Environnement:
    def __init__(self, largeur, longueur, scale):
        self.largeur = largeur
        self.longueur = longueur
        self.scale = scale
        self.robotAdapt = None
        self.listeObs = []

    def setRobot(self, robA):
        self.robotAdapt = robA
        robA.robot.refresh(TIC_SIMULATION)

    def addObstacle(self, nom, listePts):
        self.listeObs.append(Obstacle(nom, listePts))

    def refreshEnvironnement(self):
        robA = self.robotAdapt
        if robA is None:
            return
        robA.robot.refresh(TIC_SIMULATION)
        self.check_collision(robA.robot)

    def check_collision(self, robot):
        lstPointsRobot = [
            (robot.x - robot.width / 2, robot.y + robot.length / 2),
            (robot.x + robot.width / 2, robot.y + robot.length / 2),
            (robot.x + robot.width / 2, robot.y - robot.length / 2),
            (robot.x - robot.width / 2, robot.y - robot.length / 2)
        ]
        for obs in self.listeObs:
            for rx, ry in lstPointsRobot:
                for px, py in obs.points:
                    if getDistanceFromPts((rx, ry), (px, py)) < 2:
                        robot.estCrash = True
                        return
        robot.estCrash = False
