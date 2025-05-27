import math
from time import time
from src.utils import getDistanceFromPts
from src.robot.robot import Robot

class RobotSimule(Robot):
    def __init__(self, nom, x, y, width, length, vitesse_max, taille_roue, couleur="lightblue"):
        self.nom = nom
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.vitesse_max = vitesse_max
        self.taille_roue = taille_roue
        self.couleur = couleur
        self.direction = [1, 0]
        self.vitAngG = 0
        self.vitAngD = 0
        self.distance_parcourue = 0
        self.angle_parcouru = 0
        self.last_update = time()
        self.estCrash = False
        self.environnement = None
        self.img = None
        self.estSousControle = False

    def set_environnement(self, environnement):
        self.environnement = environnement

    def avancer(self, valeur):
        vitesse_angulaire = valeur / (self.taille_roue / 2)
        self.vitAngG = vitesse_angulaire
        self.vitAngD = vitesse_angulaire

    def arreter(self):
        self.vitAngG = 0
        self.vitAngD = 0

    def set_VitG(self, valeur):
        self.vitAngG = valeur

    def set_VitD(self, valeur):
        self.vitAngD = valeur

    def getDistanceParcouru(self):
        return self.distance_parcourue

    def getDistanceObstacle(self):
        if not self.environnement or not hasattr(self.environnement, 'listeObs'):
            return 1000
        min_distance = float('inf')
        cos_a, sin_a = self.direction
        robot_pos = (self.x, self.y)
        for obs in self.environnement.listeObs:
            for pt in obs.points:
                vec_x = pt[0] - robot_pos[0]
                vec_y = pt[1] - robot_pos[1]
                dot = vec_x * cos_a + vec_y * sin_a
                if dot > 0:
                    dist = getDistanceFromPts(robot_pos, pt)
                    if abs(vec_x * sin_a - vec_y * cos_a) / dist < 0.5:
                        min_distance = min(min_distance, dist)
        t_wall = float('inf')
        if cos_a != 0:
            t_wall = min(t_wall, (self.environnement.largeur - self.x) / cos_a if cos_a > 0 else -self.x / cos_a)
        if sin_a != 0:
            t_wall = min(t_wall, (self.environnement.longueur - self.y) / sin_a if sin_a > 0 else -self.y / sin_a)
        if t_wall != float('inf') and t_wall > 0:
            min_distance = min(min_distance, t_wall)
        return min_distance if min_distance != float('inf') else 1000

    def get_VitG(self):
        return self.vitAngG

    def get_VitD(self):
        return self.vitAngD

    def refresh(self, delta_t):
        delta_t = max(delta_t, 0.02)  # Assurer un minimum pour éviter des pas trop petits
        if self.estCrash:
            self.arreter()
            return
        rayon_roue = self.taille_roue / 2
        v_gauche = self.vitAngG * rayon_roue
        v_droite = self.vitAngD * rayon_roue
        v = (v_gauche + v_droite) / 2
        omega = (v_droite - v_gauche) / self.width
        theta = math.atan2(self.direction[1], self.direction[0])
        self.x += v * math.cos(theta) * delta_t
        self.y += v * math.sin(theta) * delta_t
        self.distance_parcourue += abs(v * delta_t)
        new_theta = theta + omega * delta_t
        self.direction = [math.cos(new_theta), math.sin(new_theta)]
        self.angle_parcouru += omega * delta_t

    def adjust_position(self, target_distance):
        """Corrige la position pour atteindre exactement la distance cible."""
        if abs(self.distance_parcourue - target_distance) > 0.1:  # Tolérance de 0.1 mm
            theta = math.atan2(self.direction[1], self.direction[0])
            correction = target_distance - self.distance_parcourue
            self.x += correction * math.cos(theta)
            self.y += correction * math.sin(theta)
            self.distance_parcourue = target_distance

    def adjust_angle(self, target_angle):
        """Corrige l'angle pour atteindre exactement l'angle cible (en radians)."""
        if abs(self.angle_parcouru - target_angle) > 0.001:  # Tolérance de 0.001 radian
            correction = target_angle - self.angle_parcouru
            theta = math.atan2(self.direction[1], self.direction[0])
            new_theta = theta + correction
            self.direction = [math.cos(new_theta), math.sin(new_theta)]
            self.angle_parcouru = target_angle

    def getAngleParcouru(self):
        return self.angle_parcouru

    def getDistanceRoues(self):
        return self.width

    def reset_tracking(self):
        self.distance_parcourue = 0
        self.angle_parcouru = 0
