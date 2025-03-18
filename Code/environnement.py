from time import time
from utils import normaliserVecteur

class Obstacle:
    def __init__(self, nom, points):
        self.nom, self.points = nom, points

    def get_bounding_box(self):
        min_x, max_x = min(x for x, y in self.points), max(x for x, y in self.points)
        min_y, max_y = min(y for x, y in self.points), max(y for x, y in self.points)
        return (min_x, min_y, max_x - min_x, max_y - min_y)

class Environnement:
    def __init__(self, width, length, scale):
        self.logger = getLogger(self.__class__.__name__)
        self.width = width
        self.length = length
        self.scale = scale
        self.listeRobots = []
        self.listeObs = []
        self.dicoObs = {}
        self.last_refresh = 0
        self.initBorders()

    def initBorders(self):
        lstPoints = [(0, 0), (self.width, 0), (self.width, self.length), (0, self.length)]
        for i in range(len(lstPoints)):
            x1, y1 = lstPoints[i]
            x2, y2 = lstPoints[(i + 1) % len(lstPoints)]
            self.dicoObs[(int(y1 / self.scale), int(x1 / self.scale))] = 'bordure'
            while (round(x1), round(y1)) != (round(x2), round(y2)):
                dir = normaliserVecteur((x2 - x1, y2 - y1))
                x1, y1 = (x1 + dir[0], y1 + dir[1])
                self.dicoObs[(int(y1 / self.scale), int(x1 / self.scale))] = 'bordure'

    def addObstacle(self, nom, lstPoints):
        self.listeObs.append(Obstacle(nom, lstPoints))
        for i in range(len(lstPoints)):
            x1, y1 = lstPoints[i]
            x2, y2 = lstPoints[(i + 1) % len(lstPoints)]
            self.dicoObs[(int(y1 / self.scale), int(x1 / self.scale))] = nom
            while (round(x1), round(y1)) != (round(x2), round(y2)):
                dir = normaliserVecteur((x2 - x1, y2 - y1))
                x1, y1 = (x1 + dir[0], y1 + dir[1])
                self.dicoObs[(int(y1 / self.scale), int(x1 / self.scale))] = nom

    def setRobot(self, robA):
        self.listeRobots.append(robA)

 
