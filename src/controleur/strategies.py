import math as m
from src.utils import VIT_ANG_AVAN, VIT_ANG_TOUR, getDistanceFromPts, contientBalise, TIC_CONTROLEUR
from logging import getLogger
from time import time

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
        if adaptateur.estCrash():
            self.stop(adaptateur)
            return
        self.parcouru = adaptateur.getDistanceParcourue()
        print(f"StrategieAvancer.step : parcouru={self.parcouru:.2f}/{self.distance}")

    def stop(self, adaptateur):
        if adaptateur.estCrash():
            print("StrategieAvancer.stop : Collision détectée, arrêt.")
            adaptateur.setVitAngA(0)
            return True
        if self.parcouru >= self.distance:
            print("StrategieAvancer.stop : Distance cible atteinte, arrêt.")
            adaptateur.setVitAngA(0)
            adaptateur.adjust_position(self.distance)  # Corriger la position
            return True
        print("StrategieAvancer.stop : Continue...")
        return False

class StrategieTourner:
    def __init__(self, angle):
        self.angle_cible = angle  # Angle in degrees
        self.angle_parcouru = 0
        self.start_time = None
        self.timeout = 2.0  # Timeout in seconds (2s for ~90 degrees at 57.3 deg/s)
        self.logger = getLogger(__name__)

    def start(self, adaptateur):
        adaptateur.initialise()  # Reset angle and position tracking
        self.angle_parcouru = 0
        self.start_time = time()
        if self.angle_cible > 0:
            adaptateur.tourne(-VIT_ANG_TOUR, VIT_ANG_TOUR)  # Turn left (counterclockwise)
            self.logger.debug(f"Turning left, cible: {self.angle_cible:.2f} degrés")
        else:
            adaptateur.tourne(VIT_ANG_TOUR, -VIT_ANG_TOUR)  # Turn right (clockwise)
            self.logger.debug(f"Turning right, cible: {self.angle_cible:.2f} degrés")
        self.logger.debug(f"Début de la rotation, cible: {self.angle_cible:.2f} degrés")

    def step(self, adaptateur):
        if adaptateur.estCrash():
            self.stop(adaptateur)
            return
        self.angle_parcouru = adaptateur.getAngleParcouru()
        self.logger.debug(f"Angle parcouru: {self.angle_parcouru:.2f}/{self.angle_cible:.2f} degrés")

    def stop(self, adaptateur):
        if adaptateur.estCrash():
            self.logger.info("Collision détectée, arrêt.")
            print("Collision détectée, arrêt.")
            adaptateur.arreter()
            return True
        if time() - self.start_time > self.timeout:
            self.logger.info(f"Timeout atteint ({self.timeout}s), arrêt de la rotation.")
            print(f"Timeout atteint ({self.timeout}s), arrêt de la rotation.")
            adaptateur.arreter()
            adaptateur.adjust_angle(m.radians(self.angle_cible))  # Convert to radians for adjust_angle
            return True
        if abs(self.angle_parcouru - self.angle_cible) <= 0.5:  # Tolerance of 0.5 degrees
            self.logger.info(f"Rotation terminée, arrêt. Atteint: {self.angle_parcouru:.2f} degrés")
            print(f"Rotation terminée, arrêt. Atteint: {self.angle_parcouru:.2f} degrés")
            adaptateur.arreter()
            adaptateur.adjust_angle(m.radians(self.angle_cible))  # Convert to radians for adjust_angle
            return True
        self.logger.debug("StrategieTourner.stop : Continue...")
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
        if adaptateur.estCrash():
            print("Collision détectée, arrêt du mode automatique.")
            adaptateur.arreter()
            return
        adaptateur.tourne(self.vitAngG, self.vitAngD)
        print(f"Mode auto - vitAngG={self.vitAngG}, vitAngD={self.vitAngD}")

    def stop(self, adaptateur):
        if adaptateur.estCrash():
            adaptateur.arreter()
            return True
        return False

def setStrategieCarre(longueur_cote):
    return StrategieSeq([
        StrategieAvancer(longueur_cote),
        StrategieTourner(90),  # Turn 90 degrees left
        StrategieAvancer(longueur_cote),
        StrategieTourner(90),  # Turn 90 degrees left
        StrategieAvancer(longueur_cote),
        StrategieTourner(90),  # Turn 90 degrees left
        StrategieAvancer(longueur_cote),
        StrategieTourner(90)   # Turn 90 degrees left to return to starting orientation
    ])

class StrategieArretMur:
    def __init__(self, adaptateur, distance_arret):
        self.logger = getLogger(__name__)
        self.adaptateur = adaptateur
        self.distance_arret = distance_arret
        self.parcouru = 0

    def start(self, adaptateur):
        adaptateur.initialise()
        self.parcouru = 0
        adaptateur.setVitAngA(VIT_ANG_AVAN)
        self.logger.info(f"StrategieArretMur.start : vitesse={VIT_ANG_AVAN}, distance_arret={self.distance_arret}mm")

    def step(self, adaptateur):
        if adaptateur.estCrash():
            self.stop(adaptateur)
            return
        self.parcouru = adaptateur.getDistanceParcourue()
        distance_obstacle = adaptateur.getDistanceA()
        self.logger.debug(f"StrategieArretMur.step : parcouru={self.parcouru:.2f}mm, distance_obstacle={distance_obstacle:.2f}mm")
        if distance_obstacle is None or distance_obstacle < 0:
            self.logger.warning("Distance à l'obstacle invalide, continue à avancer")
            adaptateur.setVitAngA(VIT_ANG_AVAN)
            return
        if not self.stop(adaptateur):
            adaptateur.setVitAngA(VIT_ANG_AVAN)

    def stop(self, adaptateur):
        if adaptateur.estCrash():
            adaptateur.setVitAngA(0)
            self.logger.info("StrategieArretMur.stop : collision détectée, arrêt")
            print("StrategieArretMur.stop : collision détectée, arrêt")
            return True
        distance_obstacle = adaptateur.getDistanceA()
        if distance_obstacle is None or distance_obstacle < 0:
            self.logger.warning("Distance à l'obstacle invalide, continue")
            return False
        if distance_obstacle <= self.distance_arret:
            adaptateur.setVitAngA(0)
            adaptateur.adjust_position(self.parcouru + (distance_obstacle - self.distance_arret))  # Corriger la position
            self.logger.info(f"StrategieArretMur.stop : distance_arret atteinte ({distance_obstacle:.2f}mm), arrêt")
            print(f"StrategieArretMur.stop : distance_arret atteinte ({distance_obstacle:.2f}mm), arrêt")
            return True
        self.logger.debug("StrategieArretMur.stop : continue")
        return False

class StrategieSuivreBalise:
    def __init__(self, adaptateur):
        self.logger = getLogger(self.__class__.__name__)
        self.adaptateur = adaptateur
        self.cptfalse = 0
        self.balise = False
        self.decale = 0

    def start(self, adaptateur):
        self.adaptateur.robot.estSousControle = True
        self.balise, self.decale = contientBalise(self.adaptateur.get_imageA())
        self.cptfalse = 0
        self.logger.debug("Stratégie Suivre Balise lancée")

    def step(self, adaptateur):
        if adaptateur.estCrash():
            self.stop(adaptateur)
            return
        if not self.stop(adaptateur):
            self.balise, self.decale = contientBalise(self.adaptateur.get_imageA())
            print(f"Balise détectée: {self.balise}, décalage: {self.decale}")
            if self.balise:
                adaptateur.setVitAngA(VIT_ANG_AVAN)
                if self.decale > 50:
                    adaptateur.setVitAngG(VIT_ANG_TOUR)
                    adaptateur.setVitAngD(VIT_ANG_TOUR / 2)
                elif self.decale < -50:
                    adaptateur.setVitAngG(VIT_ANG_TOUR / 2)
                    adaptateur.setVitAngD(VIT_ANG_TOUR)
                else:
                    adaptateur.setVitAngG(VIT_ANG_TOUR)
                    adaptateur.setVitAngD(VIT_ANG_TOUR)
                self.cptfalse = 0
            else:
                adaptateur.setVitAngA(0)
                self.cptfalse += 1

    def stop(self, adaptateur):
        if adaptateur.estCrash():
            adaptateur.setVitAngA(0)
            adaptateur.robot.estSousControle = False
            self.logger.info("Arrêt: collision détectée")
            return True
        if self.cptfalse > 50:
            adaptateur.setVitAngA(0)
            adaptateur.robot.estSousControle = False
            self.logger.info("Balise non détectée après 50 tentatives, arrêt")
            return True
        return False



class StrategieClavier:
    def __init__(self, adaptateur, key_map):
        self.logger = getLogger(__name__)
        self.adaptateur = adaptateur
        self.key_map = key_map
        self.linear_vel = 0  # Track linear velocity
        self.angular_vel = [0, 0]  # Track angular velocity [left, right]

    def start(self, adaptateur):
        adaptateur.initialise()
        adaptateur.setVitAngA(0)
        adaptateur.tourne(0, 0)
        self.linear_vel = 0
        self.angular_vel = [0, 0]
        self.logger.info("StrategieClavier.start: contrôle par clavier démarré")
        print("Contrôle par clavier démarré: Utilisez i (avancer), o (reculer), p (gauche), l (droite)")

    def step(self, adaptateur):
        if adaptateur.estCrash():
            self.stop(adaptateur)
            return

        # Linear movement with increased speed
        if self.key_map.get('i', False) and not self.key_map.get('o', False):
            self.linear_vel = VIT_ANG_AVAN  # Use hardcoded high speed (100 units/s)
            self.logger.debug(f"Clavier: Avancer, setVitAngA({self.linear_vel})")
        elif self.key_map.get('o', False) and not self.key_map.get('i', False):
            self.linear_vel = -VIT_ANG_AVAN  # Use hardcoded high speed (100 units/s)
            self.logger.debug(f"Clavier: Reculer, setVitAngA({self.linear_vel})")
        else:
            self.linear_vel = 0
            self.logger.debug("Clavier: Aucun mouvement linéaire")
        adaptateur.setVitAngA(self.linear_vel)

        # Angular movement (unchanged, as it works well)
        if self.key_map.get('p', False) and not self.key_map.get('l', False):
            self.angular_vel = [VIT_ANG_TOUR, -VIT_ANG_TOUR]  # Turn left
            self.logger.debug(f"Clavier: Tourner à gauche, tourne({self.angular_vel[0]}, {self.angular_vel[1]})")
        elif self.key_map.get('l', False) and not self.key_map.get('p', False):
            self.angular_vel = [-VIT_ANG_TOUR, VIT_ANG_TOUR]  # Turn right
            self.logger.debug(f"Clavier: Tourner à droite, tourne({self.angular_vel[0]}, {self.angular_vel[1]})")
        else:
            self.angular_vel = [0, 0]
            self.logger.debug("Clavier: Aucun mouvement angulaire")
        adaptateur.tourne(self.angular_vel[0], self.angular_vel[1])

        # Fallback: Update position manually with optimized speed
        if self.linear_vel != 0:
            try:
                robot = adaptateur.robot
                angle = m.atan2(robot.direction[1], robot.direction[0])
                dt = TIC_CONTROLEUR * 2  # Double the time step for faster movement
                dx = self.linear_vel * m.cos(angle) * dt
                dy = self.linear_vel * m.sin(angle) * dt
                robot.x += dx
                robot.y += dy
                self.logger.debug(f"Position update: dx={dx:.2f}, dy={dy:.2f}, new_pos=({robot.x:.2f}, {robot.y:.2f})")
            except AttributeError as e:
                self.logger.error(f"Erreur lors de la mise à jour de la position: {e}")

        # Log robot state
        try:
            position = (adaptateur.robot.x, adaptateur.robot.y)
            self.logger.debug(f"Robot position: {position}, linear_vel={self.linear_vel}, angular_vel={self.angular_vel}")
        except AttributeError:
            self.logger.error("Erreur: impossible d'accéder à la position du robot")

    def stop(self, adaptateur):
        if adaptateur.estCrash():
            adaptateur.arreter()
            self.linear_vel = 0
            self.angular_vel = [0, 0]
            self.logger.info("StrategieClavier.stop: collision détectée, arrêt")
            print("StrategieClavier.stop: collision détectée, arrêt")
            return True
        return False