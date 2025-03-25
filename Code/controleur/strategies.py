from logging import getLogger
from utils import VIT_ANG_AVAN, VIT_ANG_TOUR, getDistanceFromPts, getAngleFromVect,TIC_CONTROLEUR
from time import sleep, time
from math import atan2, cos, sin, degrees
import math

class StrategieAvancer:
    """Stratégie permettant au robot d'avancer d'une distance donnée."""

    def __init__(self, robAdapt, distance):
        self.logger = getLogger(self.__class__.__name__)
        self.distance = distance
        self.robA = robAdapt
        self.start_position = (self.robA.robot.x, self.robA.robot.y)

    def start(self):
        """Démarre la stratégie d'avancement."""
        self.logger.debug("Stratégie d'avancement démarrée.")
        self.start_position = (self.robA.robot.x, self.robA.robot.y)
        self.robA.setVitAngA(VIT_ANG_AVAN)

    def step(self):
        """Aucun traitement spécifique pendant l'avancée."""
        pass

    def stop(self):
        """Arrête la stratégie si la distance cible est atteinte."""
        current_position = (self.robA.robot.x, self.robA.robot.y)
        parcouru = getDistanceFromPts(self.start_position, current_position)
        self.logger.debug(f"Distance parcourue: {parcouru:.2f} / {self.distance:.2f}")
        if parcouru >= self.distance:
            self.robA.setVitAngA(0)
            return True
        return False

class StrategieTourner:
    """Stratégie permettant au robot de tourner d'un angle donné."""

    def __init__(self, robAdapt, angle):
        self.logger = getLogger(self.__class__.__name__)
        self.robA = robAdapt
        self.angle = angle
        self.initial_angle = None
        self.target_angle = None
        self.tolerance = math.radians(2)
        self.finished = False

    def start(self):
        """Démarre la rotation du robot."""
        self.logger.debug("Stratégie de rotation démarrée.")
        self.initial_angle = math.atan2(self.robA.robot.direction[1], self.robA.robot.direction[0])
        self.target_angle = self.initial_angle + math.radians(self.angle)

        if self.angle > 0:
            self.robA.setVitAngGA(-VIT_ANG_TOUR)
            self.robA.setVitAngDA(VIT_ANG_TOUR)
        else:
            self.robA.setVitAngGA(VIT_ANG_TOUR)
            self.robA.setVitAngDA(-VIT_ANG_TOUR)

    def step(self):
        """Corrige l'orientation du robot pour respecter l'angle cible."""
        if self.robA.robot.estCrash:
            return
        current_angle = math.atan2(self.robA.robot.direction[1], self.robA.robot.direction[0])
        diff = self.normalize_angle(current_angle - self.target_angle)
        if abs(diff) < self.tolerance:
            self.robA.robot.direction = [math.cos(self.target_angle), math.sin(self.target_angle)]
            self.robA.setVitAngA(0)
            self.finished = True

    def stop(self):
        """Retourne si la rotation est terminée."""
        return self.finished

    def normalize_angle(self, angle):
        """Normalise un angle entre -π et π."""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

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
    """Stratégie permettant au robot de se déplacer avec des vitesses angulaires définies."""

    def __init__(self, robAdapt, vitAngG, vitAngD):
        self.logger = getLogger(self.__class__.__name__)
        self.robA = robAdapt
        self.vitAngG = vitAngG
        self.vitAngD = vitAngD
        self.running = False

    def start(self):
        """Démarre le déplacement automatique."""
        self.logger.debug("Stratégie automatique démarrée.")
        self.robA.setVitAngGA(self.vitAngG)
        self.robA.setVitAngDA(self.vitAngD)
        self.running = True

    def step(self):
        """Maintient les vitesses définies, rien de plus."""
        pass

    def stop(self):
        """Arrête la stratégie si demandée explicitement (pas de condition automatique ici)."""
        return not self.running

class StrategieSeq:
    """Séquence de stratégies exécutées les unes après les autres."""
    def __init__(self, strategies, robAdapt):
        self.strategies = strategies
        self.robA = robAdapt
        self.current = 0

    def start(self):
        if self.current < len(self.strategies):
            self.strategies[self.current].start()

    def step(self):
        if self.current < len(self.strategies):
            self.strategies[self.current].step()
            if self.strategies[self.current].stop():
                self.current += 1
                if self.current < len(self.strategies):
                    self.strategies[self.current].start()

    def stop(self):
        return self.current >= len(self.strategies)
        

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

