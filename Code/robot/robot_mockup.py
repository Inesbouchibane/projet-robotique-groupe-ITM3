from .robot import Robot
from logging import getLogger
from random import uniform
from math import cos, sin, atan2

class RobotMockup(Robot):
    """Classe représentant une version simulée simplifiée (mockup) d'un robot pour tests."""

    def __init__(self, nom, x, y, width, length, height, rayonRoue, couleur):
        super().__init__(nom, x, y, width, length, height, rayonRoue, couleur)
        self.logger = getLogger(self.__class__.__name__)
        self.simulated_noise = 0.1

    def refresh(self, duree):
        if self.estCrash:
            self.logger.debug(f"Robot mockup {self.nom} est en collision, mise à jour ignorée.")
            return
        vg = self.getVitesseG()  # Vitesse linéaire gauche
        vd = self.getVitesseD()  # Vitesse linéaire droite
        vitesse = (vg + vd) / 2 + uniform(-self.simulated_noise, self.simulated_noise)
        
        if abs(vg - vd) < 1e-5:  # Mouvement droit
            self.x += self.direction[0] * vitesse * duree * 10
            self.y += self.direction[1] * vitesse * duree * 10
        else:  # Rotation
            omega = (vd - vg) / self.width  # Vitesse angulaire de rotation
            angle = atan2(self.direction[1], self.direction[0]) + omega * duree
            self.direction = [cos(angle), sin(angle)]
            self.x += self.direction[0] * vitesse * duree * 10
            self.y += self.direction[1] * vitesse * duree * 10
        
        print(f"Refresh: vg={vg:.2f}, vd={vd:.2f}, direction={self.direction}, pos=({self.x:.3f}, {self.y:.3f})")
        self.logger.info(f"Robot mockup {self.nom} déplacé à ({self.x:.1f}, {self.y:.1f})")

    def getDistance(self, env=None):
        if not env:
            self.logger.warning("Aucun environnement fourni, distance simulée.")
        simulated_distance = uniform(10, 100)
        self.logger.debug(f"Distance simulée pour {self.nom}: {simulated_distance:.1f}")
        return simulated_distance

    def setVitAng(self, vit):
        self.vitAngD = vit + uniform(-0.05, 0.05)
        self.vitAngG = vit + uniform(-0.05, 0.05)
        self.logger.debug(f"Vitesse angulaire simulée pour {self.nom}: G={self.vitAngG:.2f}, D={self.vitAngD:.2f}")

