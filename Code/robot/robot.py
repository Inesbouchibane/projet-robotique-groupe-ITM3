from logging import getLogger
from math import cos, sin, pi, sqrt, atan2
from utils import getAngleFromVect, getDistanceFromPts, normaliserVecteur, 
VIT_ANG_AVAN, VIT_ANG_TOUR
from time import sleep


class Robot:
    def __init__(self, nom, x, y, width, length, height, rayonRoue, couleur):
        self.logger = getLogger(self.__class__.__name__)
        self.nom = nom
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.height = height
        self.rayonRoue = rayonRoue
        self.couleur = couleur
        self.direction = [0, -1]  # Direction initiale: vers le bas
        self._vitAngG = 0
        self._vitAngD = 0
        self.estSousControle = False
        self.estCrash = False
        self.last_x = x
        self.last_y = y
