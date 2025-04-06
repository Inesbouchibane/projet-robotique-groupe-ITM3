import math as m
from src.utils import VIT_ANG_AVAN, VIT_ANG_TOUR, getDistanceFromPts
from logging import getLogger

class StrategieAvancer:
    def __init__(self, distance):
        self.distance = distance
        self.parcouru = 0
        
    def start(self, adaptateur):
        adaptateur.initialise()
        self.parcouru = 0
        adaptateur.setVitAngA(VIT_ANG_AVAN)
        print(f"StrategieAvancer.start : distance cible={self.distance}, vitesse={VIT_ANG_AVAN}")

    def step(self, adaptateur):
        self.parcouru = adaptateur.getDistanceParcourue()
        distance_obstacle = adaptateur.getDistanceObstacle()
        print(f"StrategieAvancer.step : parcouru={self.parcouru:.2f}/{self.distance}, "
              f"distance_obstacle={distance_obstacle:.2f}")

    def stop(self, adaptateur):
        distance_obstacle = adaptateur.getDistanceObstacle()
        if distance_obstacle < 20:
            print("StrategieAvancer.stop : Obstacle détecté, arrêt.")
            adaptateur.setVitAngA(0)
            return True
        if self.parcouru >= self.distance:
            print("StrategieAvancer.stop : Distance cible atteinte, arrêt.")
            adaptateur.setVitAngA(0)
            return True
        print("StrategieAvancer.stop : Continue...")
        return False

class StrategieTourner:
    def __init__(self, angle):
        self.angle_cible = m.radians(angle)
        self.angle_parcouru = 0

    def start(self, adaptateur):
        adaptateur.initialise()
        self.angle_parcouru = 0
        if self.angle_cible > 0:
            adaptateur.tourne(VIT_ANG_TOUR, -VIT_ANG_TOUR)
        else:
            adaptateur.tourne(-VIT_ANG_TOUR, VIT_ANG_TOUR)
        print(f"Début de la rotation, cible: {m.degrees(self.angle_cible)} degrés")

    def step(self, adaptateur):
        self.angle_parcouru = adaptateur.getAngleParcouru()
        print(f"Angle parcouru: {m.degrees(self.angle_parcouru):.2f}/{m.degrees(self.angle_cible)} degrés")

    def stop(self, adaptateur):
        if adaptateur.getDistanceObstacle() < 20:
            print("Obstacle détecté, arrêt.")
            adaptateur.arreter()
            return True
        if abs(self.angle_parcouru) >= abs(self.angle_cible) - 0.01:
            print("Rotation terminée, arrêt.")
            adaptateur.arreter()
            return True
        return False
    
class StrategieSeq:
    def __init__(self, liste_strategies):
        self.liste_strategies = liste_strategies
        self.index = 0
    
    def start(self, adaptateur):
        if self.index < len(self.liste_strategies):
            self.liste_strategies[self.index].start(adaptateur)
    
    def step(self, adaptateur):
        if self.index < len(self.liste_strategies):
            print(f"Exécution de la stratégie {self.index + 1}/{len(self.liste_strategies)}")
            strategie = self.liste_strategies[self.index]
            if not strategie.stop(adaptateur):
                strategie.step(adaptateur)
            else:
                print(f"Stratégie {self.index + 1} terminée.")
                self.index += 1
                if self.index < len(self.liste_strategies):
                    self.liste_strategies[self.index].start(adaptateur)

    def stop(self, adaptateur):
        return self.index >= len(self.liste_strategies)

class StrategieAuto:
    def __init__(self, vitAngG, vitAngD):
        self.vitAngG = vitAngG
        self.vitAngD = vitAngD

    def start(self, adaptateur):
        adaptateur.initialise()
        adaptateur.tourne(self.vitAngG, self.vitAngD)
        print(f"Début de la stratégie auto avec vitAngG={self.vitAngG}, vitAngD={self.vitAngD}")

    def step(self, adaptateur):
        if adaptateur.getDistanceObstacle() < 20:
            print("Obstacle ou mur détecté, arrêt du mode automatique.")
            adaptateur.arreter()
            return
        adaptateur.tourne(self.vitAngG, self.vitAngD)
        print(f"Mode auto - vitAngG={self.vitAngG}, vitAngD={self.vitAngD}, "
              f"Distance obstacle: {adaptateur.getDistanceObstacle():.2f}")

    def stop(self, adaptateur):
        if adaptateur.getDistanceObstacle() < 20:
            adaptateur.arreter()
            return True
        return False

def setStrategieCarre(longueur_cote):
    return StrategieSeq([
        StrategieAvancer(longueur_cote),
        StrategieTourner(90),
        StrategieAvancer(longueur_cote),
        StrategieTourner(90),
        StrategieAvancer(longueur_cote),
        StrategieTourner(90),
        StrategieAvancer(longueur_cote),
        StrategieTourner(90)
    ])
