from logging import getLogger
from math import cos, sin, pi, sqrt, atan2
from utils import getAngleFromVect, getDistanceFromPts, normaliserVecteur, VIT_ANG_AVAN, VIT_ANG_TOUR
from time import sleep

class Robot:
    def _init_(self, nom, x, y, width, length, height, rayonRoue, couleur):
        self.logger = getLogger(self._class.name_)
        self.nom = nom
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.height = height
        self.rayonRoue = rayonRoue
        self.couleur = couleur
        self.direction = [0, -1]  # Initial direction: down
        self._vitAngG = 0
        self._vitAngD = 0
        self.estSousControle = False
        self.estCrash = False
        self.last_x = x
        self.last_y = y

    def refresh(self, duree):
        if self.estCrash:
            self.logger.debug(f"Robot {self.nom} is crashed, skipping refresh")
            return
        vg = self.getVitesseG()  # Left wheel linear speed
        vd = self.getVitesseD()  # Right wheel linear speed
        self.logger.debug(f"Robot {self.nom} - Refresh: vg={vg}, vd={vd}, direction={self.direction}, position=({self.x}, {self.y})")

        if abs(vg - vd) < 1e-5:  # Move straight
            norm_dir = normaliserVecteur(self.direction)
            self.direction = norm_dir
            self.x += norm_dir[0] * vg * duree
            self.y += norm_dir[1] * vg * duree
        else:  # Turn
            R = self.width * (vg + vd) / (2 * (vd - vg)) if vd != vg else float('inf')
            omega = (vd - vg) / self.width
            angle = self.getAngle() + omega * duree
            self.direction = [cos(angle), sin(angle)]
            ICC_x = self.x - R * sin(self.getAngle())
            ICC_y = self.y + R * cos(self.getAngle())
            self.x = ICC_x + R * sin(angle)
            self.y = ICC_y - R * cos(angle)

        # Check for movement
        if abs(self.x - self.last_x) > 1 or abs(self.y - self.last_y) > 1:
            self.logger.info(f"Robot {self.nom} moved to ({self.x:.1f}, {self.y:.1f})")
            self.last_x = self.x
            self.last_y = self.y

    def getAngle(self):
        return atan2(self.direction[1], self.direction[0])

    @property
    def vitAngG(self):
        return self._vitAngG

    @vitAngG.setter
    def vitAngG(self, vit):
        self._vitAngG = vit
        self.logger.debug(f"Vitesse roueG set à {vit} pour {self.nom}")

    @property
    def vitAngD(self):
        return self._vitAngD

    @vitAngD.setter
    def vitAngD(self, vit):
        self._vitAngD = vit
        self.logger.debug(f"Vitesse roueD set à {vit} pour {self.nom}")

    def setVitAng(self, vit):
        self.vitAngD = vit
        self.vitAngG = vit
        self.logger.debug(f"Vitesse globale set à {vit} pour {self.nom}")

    def getVitesseG(self):
        return self.vitAngG * self.rayonRoue

    def getVitesseD(self):
        return self.vitAngD * self.rayonRoue

    def getVitesse(self):
        return (self.getVitesseD() + self.getVitesseG()) / 2

    def getDistance(self, env):
        x1, y1 = (self.x + self.direction[0] * (self.length/2), self.y + self.direction[1] * (self.length/2))
        x2, y2 = x1, y1
        dirNorm = normaliserVecteur(self.direction)
        while (int(y2/env.scale), int(x2/env.scale)) not in env.dicoObs:
            x2, y2 = (x2 + dirNorm[0], y2 + dirNorm[1])
        return sqrt((x2 - x1)*2 + (y2 - y1)*2)

    def avoidObstacle(self, env):
        distance = self.getDistance(env)
        if distance < 50:  # If an obstacle is close
            self.logger.debug("Obstacle detected, turning...")
            self.vitAngG = -VIT_ANG_TOUR  # Turn left
            self.vitAngD = VIT_ANG_TOUR
            sleep(0.5)  # Turn for half a second