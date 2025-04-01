from logging import getLogger
from utils import VIT_ANG_AVAN, VIT_ANG_TOUR, getDistanceFromPts, getAngleFromVect,TIC_CONTROLEUR
from time import sleep, time
from math import atan2, cos, sin, degrees
import math

class StrategieAvancer:
    def __init__(self, distance):
        self.distance = distance
        self.parcouru = 0
        
    def start(self, adaptateur):
        adaptateur.initialise()
        self.parcouru = 0
        adaptateur.setVitAngA(VIT_ANG_AVAN)
        print(f"Début de l'avancée, cible: {self.distance}")

    def step(self, adaptateur):
        self.parcouru = adaptateur.getDistanceParcourue()
        position = adaptateur.getPosition()
        direction = m.degrees(m.atan2(adaptateur.getDirection()[1], adaptateur.getDirection()[0]))
        print(f"Position: {position}, Direction: {direction:.2f}°, J'ai parcouru: {self.parcouru:.2f}/{self.distance}")

    def stop(self, adaptateur):
        if adaptateur.getDistanceObstacle() < 20:
            print("Obstacle détecté, arrêt.")
            adaptateur.setVitAngA(0)
            return True
        if self.parcouru >= self.distance:
            print("Distance cible atteinte, arrêt.")
            adaptateur.setVitAngA(0)
            return True
        return False


class StrategieTourner:
    def __init__(self, angle):
        self.angle_cible = m.radians(angle)  
        self.angle_parcouru = 0

    def start(self, adaptateur):
        adaptateur.initialise()
        self.angle_parcouru = 0
        if self.angle_cible > 0:  # Tourne a gauche
            adaptateur.setVitAngGA(-VIT_ANG_TOUR)
            adaptateur.setVitAngDA(VIT_ANG_TOUR)
        else:  # Tourne a droite
            adaptateur.setVitAngGA(VIT_ANG_TOUR)
            adaptateur.setVitAngDA(-VIT_ANG_TOUR)
        print(f"Début de la rotation, cible: {m.degrees(self.angle_cible)} degrés")

    def step(self, adaptateur):
        self.angle_parcouru = adaptateur.getAngleParcouru()
        position = adaptateur.getPosition()
        direction = m.degrees(m.atan2(adaptateur.getDirection()[1], adaptateur.getDirection()[0]))
        print(f"Position: {position}, Direction: {direction:.2f}°, Angle parcouru:{m.degrees(self.angle_parcouru):.2f}/{m.degrees(self.angle_cible)} degrés")

    def stop(self, adaptateur):
        if adaptateur.getDistanceObstacle() < 20:
            print("Obstacle détecté, arrêt.")
            adaptateur.setVitAngGA(0)
            adaptateur.setVitAngDA(0)
            return True
        if abs(self.angle_parcouru) >= abs(self.angle_cible) - 0.01:  #  tolerance
            print("Rotation terminée, arrêt.")
            adaptateur.setVitAngGA(0)
            adaptateur.setVitAngDA(0)
            # Inline snapping logic from snap_direction
            theta = m.atan2(adaptateur.getDirection()[1], adaptateur.getDirection()[0])
            theta_deg = m.degrees(theta) % 360
            if 45 <= theta_deg < 135:
                adaptateur.robot.direction = [0, 1]  # Up
            elif 135 <= theta_deg < 225:
                adaptateur.robot.direction = [-1, 0]  # Left
            elif 225 <= theta_deg < 315:
                adaptateur.robot.direction = [0, -1]  # Down
            else:
                adaptateur.robot.direction = [1, 0]  # Right
            print(f"Direction ajustée à: {m.degrees(m.atan2(adaptateur.getDirection()[1], adaptateur.getDirection()[0])):.2f}°")
            return True
        return False


def setStrategieCarre(robAdapt, longueur_cote):
    """Crée une séquence de stratégies pour tracer un carré."""
    return StrategieSeq([
        StrategieAvancer(robAdapt, longueur_cote),
        StrategieTourner(robAdapt, 90),
        StrategieAvancer(robAdapt, longueur_cote),
        StrategieTourner(robAdapt, 90),
        StrategieAvancer(robAdapt, longueur_cote),
        StrategieTourner(robAdapt, 90),
        StrategieAvancer(robAdapt, longueur_cote),
        StrategieTourner(robAdapt, 90)
    ], robAdapt)

class StrategieVersMur:
    """Stratégie permettant au robot d'avancer vers le mur le plus proche."""

    def __init__(self, robAdapt):
        self.logger = getLogger(self.__class__.__name__)
        self.robA = robAdapt
        self.target_angle = 0
        self.step_phase = 0
        self.strat_tourner = None
        self.strat_avancer = None

    def start(self):
        """Détecte le mur le plus proche et oriente le robot vers lui."""
        self.logger.debug("Détection du mur le plus proche.")
        directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        min_dist = float('inf')
        target_dir = (0, -1)

        for dir in directions:
            self.robA.robot.direction = dir
            dist = self.robA.robot.getDistance(self.robA.env)
            if dist < min_dist:
                min_dist = dist
                target_dir = dir

        self.target_angle = getAngleFromVect(self.robA.robot.direction, target_dir)
        self.step_phase = 1
        self.strat_tourner = StrategieTourner(self.robA, self.target_angle)
        self.strat_tourner.start()

    def step(self):
        """Exécute la rotation puis l'avance vers le mur."""
        if self.step_phase == 1:
            self.strat_tourner.step()
            if self.strat_tourner.stop():
                self.step_phase = 2
                self.strat_avancer = StrategieAvancer(self.robA, 200)
                self.strat_avancer.start()
        elif self.step_phase == 2:
            self.strat_avancer.step()

    def stop(self):
        """Retourne si la stratégie est terminée."""
        return self.step_phase == 2 and self.strat_avancer.stop()

class StrategieAuto:
    def __init__(self, vitAngG, vitAngD):
        self.vitAngG = vitAngG
        self.vitAngD = vitAngD

    def start(self, adaptateur):
        adaptateur.setVitAngGA(self.vitAngG)
        adaptateur.setVitAngDA(self.vitAngD)
        print(f"Début de la stratégie auto avec vitAngG={self.vitAngG}, vitAngD={self.vitAngD}")

    def step(self, adaptateur):
        adaptateur.setVitAngGA(self.vitAngG)
        adaptateur.setVitAngDA(self.vitAngD)
        print(f"Step - Envoi : vitAngG={self.vitAngG}, vitAngD={self.vitAngD}, Après : G={adaptateur.getVitG()}, D={adaptateur.getVitD()}")

    def stop(self, adaptateur):
        return False  # Ne s’arrête que via ESC
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

class StrategieSuivreBalise:
    """Stratégie pour faire suivre une balise au robot."""
    def __init__(self, adaptateur, balise, vitesse_max=VIT_ANG_AVAN, vitesse_tour=VIT_ANG_TOUR, tolerance_angle=0.1, distance_arret=10):
        self.adaptateur = adaptateur
        self.balise = balise
        self.vitesse_max = vitesse_max  # Vitesse pour avancer (ex. 50)
        self.vitesse_tour = vitesse_tour  # Vitesse pour tourner (ex. 30)
        self.tolerance_angle = tolerance_angle  # Tolérance en radians (≈5.7°)
        self.distance_arret = distance_arret  # Distance pour considérer la balise atteinte
        self.running = False

    def step(self):
        """Effectue une étape de la stratégie."""
        if not self.running:
            return

        robot = self.adaptateur.robot
        # Calcul de la distance à la balise
        distance = getDistanceFromPts((robot.x, robot.y), (self.balise.x, self.balise.y))
        if distance < self.distance_arret:
            self.stop()
            print(f"Balise atteinte ! Distance = {distance:.2f}")
            return

        # Calcul de l'angle vers la balise
        dx = self.balise.x - robot.x
        dy = self.balise.y - robot.y
        angle_cible = atan2(dy, dx)
        angle_actuel = atan2(robot.direction[1], robot.direction[0])
        angle_diff = (angle_cible - angle_actuel + 3.14159) % (2 * 3.14159) - 3.14159

        # Ajustement proportionnel de la vitesse en fonction de l'angle
        facteur_vitesse = min(1.0, abs(angle_diff) / 0.5)  # Réduit la vitesse si l'angle est petit
        vitesse_tour_effective = self.vitesse_tour * facteur_vitesse

        # Si l'angle est trop grand, tourner
        if abs(angle_diff) > self.tolerance_angle:
            if angle_diff > 0:
                # Tourner à droite
                self.adaptateur.setVitAngGA(-vitesse_tour_effective / 2)
                self.adaptateur.setVitAngDA(vitesse_tour_effective)
                print(f"Tourne droite, angle_diff={degrees(angle_diff):.1f}°, vitesse_tour={vitesse_tour_effective:.2f}")
            else:
                # Tourner à gauche
                self.adaptateur.setVitAngGA(vitesse_tour_effective)
                self.adaptateur.setVitAngDA(-vitesse_tour_effective / 2)
                print(f"Tourne gauche, angle_diff={degrees(angle_diff):.1f}°, vitesse_tour={vitesse_tour_effective:.2f}")
        else:
            # Avancer tout droit vers la balise
            self.adaptateur.setVitAngA(self.vitesse_max)
            print(f"Avance vers la balise, angle_diff={degrees(angle_diff):.1f}°, distance={distance:.2f}")

    def start(self):
        """Démarre la stratégie."""
        self.running = True
        print("Stratégie Suivre Balise démarrée.")

    def stop(self):
        """Arrête la stratégie."""
        self.running = False
        self.adaptateur.setVitAngA(0)
        print("Stratégie Suivre Balise arrêtée.")

