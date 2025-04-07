import math
from time import time
from .robot import Robot

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
        self.direction = [1, 0]  # Initial direction (right)
        self.vitAngG = 0
        self.vitAngD = 0
        self.distance_parcourue = 0
        self.angle_parcouru = 0
        self.last_update = time()
        self.estCrash = False

    def avancer(self, valeur):
        vitesse_angulaire = valeur / (self.taille_roue / 2)  # Correction : rayon, pas diamètre
        self.vitAngG = vitesse_angulaire
        self.vitAngD = vitesse_angulaire

    def arreter(self):
        self.vitAngG = 0
        self.vitAngD = 0

    def set_VitG(self, valeur):
     # Correction : rayon
        self.vitAngG = valeur

    def set_VitD(self, valeur):
          # Correction : rayon
        self.vitAngD = valeur

    def getDistanceParcouru(self):
        return self.distance_parcourue

    def getDistanceObstacle(self):
        return float('inf')

    def get_VitG(self):
        return self.vitAngG

    def get_VitD(self):
        return self.vitAngD

    def refresh(self, delta_t=None):
        if delta_t is None:
            current_time = time()
            delta_t = current_time - self.last_update
            self.last_update = current_time
        delta_t = max(delta_t, 0.02)  # Garantir un delta_t minimum (TIC_SIMULATION)

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

        # Ajout pour débogage
        print(f"vitAngG={self.vitAngG}, vitAngD={self.vitAngD}, v_gauche={v_gauche}, v_droite={v_droite}, omega={omega}, delta_t={delta_t}, theta={theta:.3f}, new_theta={new_theta:.3f}")

    def getAngleParcouru(self):
        return self.angle_parcouru

    def getDistanceRoues(self):
        return self.width

    def reset_tracking(self):
        self.distance_parcourue = 0
        self.angle_parcouru = 0
   
    def dessine (self,b) :
       if (b) : 
 
