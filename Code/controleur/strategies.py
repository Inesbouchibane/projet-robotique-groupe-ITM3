from logging import getLogger
from utils import VIT_ANG_AVAN, VIT_ANG_TOUR, getDistanceFromPts
from time import sleep, time
from utils import getAngleFromVect

import math

class StrategieAvancer:
    def __init__(self, robAdapt, distance):
        self.logger = getLogger(self.__class__.__name__)
        self.distance = distance
        self.robA = robAdapt
        self.start_position = (self.robA.robot.x, self.robA.robot.y)

    def start(self):
        self.logger.debug("Stratégie avancer démarrée")
        self.start_position = (self.robA.robot.x, self.robA.robot.y)
        self.robA.setVitAngA(VIT_ANG_AVAN)

    def step(self):
        # Aucun traitement particulier pendant l'avancée
        pass

    def stop(self):
        current_position = (self.robA.robot.x, self.robA.robot.y)
        parcouru = getDistanceFromPts(self.start_position, current_position)
        self.logger.debug("Distance parcourue: %.2f (cible: %.2f)", parcouru, self.distance)
        if parcouru >= self.distance:
            self.robA.setVitAngA(0)
            return True
        return False

class StrategieTourner:
    def __init__(self, robAdapt, angle):
        self.logger = getLogger(self.__class__.__name__)
        self.robA = robAdapt
        self.angle = angle  # Angle en degrés (90° pour le carré)
        self.initial_angle = None
        self.target_angle = None
        self.tolerance = math.radians(2)  # Tolérance de 2 degrés
        self.finished = False

    def start(self):
        self.logger.debug("Stratégie tourner lancée")
        self.initial_angle = math.atan2(self.robA.robot.direction[1], self.robA.robot.direction[0])
        self.target_angle = self.initial_angle + math.radians(self.angle)
        # Pour une rotation positive (sens anti-horaire), on inverse les commandes
        if self.angle > 0:
            self.robA.setVitAngGA(-VIT_ANG_TOUR)
            self.robA.setVitAngDA(VIT_ANG_TOUR)
        else:
            self.robA.setVitAngGA(VIT_ANG_TOUR)
            self.robA.setVitAngDA(-VIT_ANG_TOUR)

    def step(self):
        if self.robA.robot.estCrash:
            return
        current_angle = math.atan2(self.robA.robot.direction[1], self.robA.robot.direction[0])
        diff = self.normalize_angle(current_angle - self.target_angle)
        self.logger.debug("Différence angulaire: %.4f radians", diff)
        if abs(diff) < self.tolerance:
            # Correction de l'orientation pour atteindre exactement le target
            self.robA.robot.direction = [math.cos(self.target_angle), math.sin(self.target_angle)]
            self.robA.setVitAngA(0)
            self.finished = True
            self.logger.debug("Rotation terminée. Orientation corrigée.")

    def stop(self):
        return self.finished

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

class StrategieAuto:
    def __init__(self, robAdapt, vitAngG, vitAngD):
        self.logger = getLogger(self.__class__.__name__)
        self.robA = robAdapt
        self.vitAngG = vitAngG
        self.vitAngD = vitAngD
        self.running = False
        self.avoiding = False
        self.avoid_start_time = None
        self.avoid_duration = 0.5  # Durée d'évitement en secondes
        self.robA.initialise()

    def start(self):
        self.logger.debug("Stratégie automatique démarrée avec vitAngG: %f, vitAngD: %f", self.vitAngG, self.vitAngD)
        self.running = True
        self.avoiding = False
        self.robA.setVitAngGA(self.vitAngG)
        self.robA.setVitAngDA(self.vitAngD)
        self.robA.initialise()

    def step(self):
        if self.running and not self.robA.robot.estCrash:
            distance = self.robA.getDistanceA()
            self.logger.debug("Distance à l'obstacle: %f", distance)
            if distance < 50:
                if not self.avoiding:
                    self.logger.debug("Obstacle détecté, démarrage de l'évitement")
                    self.avoid_start_time = time()
                    self.avoiding = True
                    # Choix du virage d'évitement en fonction des vitesses de base
                    if self.vitAngG < self.vitAngD:
                        # Si la roue gauche est plus lente, le robot tourne naturellement vers la gauche.
                        # Pour éviter l'obstacle, on force un virage plus prononcé vers la droite.
                        self.robA.setVitAngGA(abs(VIT_ANG_TOUR))
                        self.robA.setVitAngDA(-abs(VIT_ANG_TOUR))
                    else:
                        # Si la roue droite est plus lente, le robot tourne naturellement vers la droite.
                        # Pour éviter l'obstacle, on force un virage plus prononcé vers la gauche.
                        self.robA.setVitAngGA(-abs(VIT_ANG_TOUR))
                        self.robA.setVitAngDA(abs(VIT_ANG_TOUR))
            else:
                if not self.avoiding:
                    self.robA.setVitAngGA(self.vitAngG)
                    self.robA.setVitAngDA(self.vitAngD)
            if self.avoiding:
                if time() - self.avoid_start_time >= self.avoid_duration:
                    self.logger.debug("Fin de l'évitement, reprise de la vitesse automatique")
                    self.avoiding = False
                    self.robA.setVitAngGA(self.vitAngG)
                    self.robA.setVitAngDA(self.vitAngD)

    def stop(self):
        return False  # La stratégie automatique ne s'arrête pas d'elle-même

class StrategieSeq:
    def __init__(self, liste_strategies, robAdapt):
        self.liste_strategies = liste_strategies
        self.robA = robAdapt
        self.index = 0

    def start(self):
        if self.index < len(self.liste_strategies):
            self.liste_strategies[self.index].start()

    def step(self):
        if self.index < len(self.liste_strategies):
            self.liste_strategies[self.index].step()

    def stop(self):
        if self.index >= len(self.liste_strategies):
            return True
        if self.liste_strategies[self.index].stop():
            self.index += 1
            if self.index < len(self.liste_strategies):
                self.liste_strategies[self.index].start()
            else:
                return True
        return False

def setStrategieCarre(robAdapt, longueur_cote):
    # Un carré se compose de 4 segments d'avancée et 4 rotations de 90° chacune.
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
    
    
# controleur/strategies.py
class StrategieVersMur:
    def __init__(self, robAdapt):
        self.logger = getLogger(self.__class__.__name__)
        self.robA = robAdapt
        self.target_angle = 0
        self.step_phase = 0  # 0: détection, 1: rotation, 2: avancement
        self.strat_tourner = None
        self.strat_avancer = None

    def start(self):
        self.logger.debug("Détection du mur le plus proche")
        directions = [
            (0, -1), (1, -1), (1, 0), (1, 1),
            (0, 1), (-1, 1), (-1, 0), (-1, -1)
        ]
        min_dist = float('inf')
        target_dir = (0, -1)
        for dir in directions:
            self.robA.robot.direction = dir  # Met la direction temporairement
            dist = self.robA.robot.getDistance(self.robA.env)  # Appelle avec 2 arguments

            if dist < min_dist:
                min_dist = dist
                target_dir = dir
        current_vect = self.robA.robot.direction
        angle = getAngleFromVect(current_vect, target_dir)
        self.target_angle = angle
        self.step_phase = 1
        self.strat_tourner = StrategieTourner(self.robA, self.target_angle)
        self.strat_tourner.start()

    def step(self):
        if self.step_phase == 1:
            self.strat_tourner.step()
            if self.strat_tourner.stop():
                self.step_phase = 2
                self.strat_avancer = StrategieAvancer(self.robA, 200)  # Avance de 200 unités
                self.strat_avancer.start()
        elif self.step_phase == 2:
            self.strat_avancer.step()

    def stop(self):
        if self.step_phase == 2:
            return self.strat_avancer.stop()
        return False

