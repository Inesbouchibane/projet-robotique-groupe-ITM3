from src.utils import getDistanceFromPts, TIC_SIMULATION
from .obstacle import Obstacle

class Environnement:
    def __init__(self, largeur, longueur, scale):
        self.largeur = largeur  # Largeur de la fenêtre
        self.longueur = longueur  # Hauteur de la fenêtre
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
        # Calculer la boîte englobante du robot
        robot_bb = (
            robot.x - robot.width / 2, robot.y - robot.length / 2,
            robot.width, robot.length
        )
        robot_points = [
            (robot.x - robot.width / 2, robot.y + robot.length / 2),
            (robot.x + robot.width / 2, robot.y + robot.length / 2),
            (robot.x + robot.width / 2, robot.y - robot.length / 2),
            (robot.x - robot.width / 2, robot.y - robot.length / 2)
        ]

        # Vérification des limites de la fenêtre (murs)
        for rx, ry in robot_points:
            if rx < 0 or rx > self.largeur or ry < 0 or ry > self.longueur:
                robot.estCrash = True
                robot.arreter()  # Arrête le robot immédiatement
                print(f"Collision avec un mur à ({rx:.1f}, {ry:.1f}) ! Robot arrêté.")
                return

        # Vérification des collisions avec les obstacles
        for obs in self.listeObs:
            obs_bb = obs.get_bounding_box()
            if not self.bbox_intersect(robot_bb, obs_bb):
                continue

            for rx, ry in robot_points:
                for px, py in obs.points:
                    if getDistanceFromPts((rx, ry), (px, py)) < 5:
                        robot.estCrash = True
                        robot.arreter()  # Arrête le robot immédiatement
                        print(f"Collision avec un obstacle à ({rx:.1f}, {ry:.1f}) ! Robot arrêté.")
                        return

        robot.estCrash = False

    def bbox_intersect(self, bb1, bb2):
        """Vérifie si deux boîtes englobantes s'intersectent."""
        x1, y1, w1, h1 = bb1
        x2, y2, w2, h2 = bb2
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)