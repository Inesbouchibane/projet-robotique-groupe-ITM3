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
        self.angle_cible = 25 # Angle en degrés
        self.angle_parcouru = 0
        self.start_time = None
        self.timeout = 2.0  # Durée max d’une rotation (en secondes)
        self.logger = getLogger(__name__)

    def start(self, adaptateur):
        adaptateur.initialise()  # Réinitialise les encodeurs
        self.angle_parcouru = 0
        self.start_time = time()
        if self.angle_cible > 0:
            adaptateur.tourne(-VIT_ANG_TOUR, VIT_ANG_TOUR)  # Tourner à gauche
            self.logger.debug(f"Turning left, cible: {self.angle_cible:.2f} degrés")
        else:
            adaptateur.tourne(VIT_ANG_TOUR, -VIT_ANG_TOUR)  # Tourner à droite
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
            adaptateur.initialise()  # Reset pour stratégie suivante
            return True

        angle_parcouru_deg = m.degrees(self.angle_parcouru)

        if abs(angle_parcouru_deg - self.angle_cible) <= 0.5:
            self.logger.info(f"Rotation terminée, arrêt. Atteint: {angle_parcouru_deg:.2f} degrés")
            print(f"Rotation terminée, arrêt. Atteint: {angle_parcouru_deg:.2f} degrés")
            adaptateur.arreter()
            adaptateur.adjust_angle(m.radians(self.angle_cible))
            adaptateur.initialise()
            return True

        if time() - self.start_time > self.timeout:
            self.logger.info(f"Timeout atteint ({self.timeout}s), arrêt de la rotation.")
            print(f"Timeout atteint ({self.timeout}s), arrêt de la rotation.")
            adaptateur.arreter()
            adaptateur.adjust_angle(m.radians(self.angle_cible))
            adaptateur.initialise()
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
        self.compteur_detection = 0
        self.confirmation_detection = 5  # nombre de cycles consécutifs à confirmer l'obstacle

    def start(self, adaptateur):
        adaptateur.initialise()
        self.parcouru = 0
        self.compteur_detection = 0
        adaptateur.setVitAngA(VIT_ANG_AVAN)
        self.logger.info(f"[Start] Avance avec V={VIT_ANG_AVAN} jusqu’à {self.distance_arret} mm")

    def step(self, adaptateur):
        if adaptateur.estCrash():
            self.logger.warning("[Step] Collision détectée")
            self.stop(adaptateur)
            return

        self.parcouru = adaptateur.getDistanceParcourue()
        distance_obstacle = adaptateur.getDistanceA()

        if distance_obstacle is None or distance_obstacle < 5 or distance_obstacle > 8190:
            self.logger.warning("[Step] Mesure capteur invalide (None ou hors plage)")
            self.compteur_detection = 0
            return

        self.logger.debug(f"[Step] Parcouru={self.parcouru:.1f}mm, Obstacle={distance_obstacle:.1f}mm")

        if distance_obstacle <= self.distance_arret:
            self.compteur_detection += 1
            self.logger.debug(f"[Step] Détection #{self.compteur_detection}/{self.confirmation_detection}")
        else:
            self.compteur_detection = 0

        if not self.stop(adaptateur):
            adaptateur.setVitAngA(VIT_ANG_AVAN)

    def stop(self, adaptateur):
        if adaptateur.estCrash():
            adaptateur.setVitAngA(0)
            self.logger.info("[Stop] Arrêt suite à collision")
            print("[Stop] Collision détectée")
            return True

        distance_obstacle = adaptateur.getDistanceA()
        if distance_obstacle is None or distance_obstacle < 5 or distance_obstacle > 8190:
            return False

        if self.compteur_detection >= self.confirmation_detection:
            adaptateur.setVitAngA(0)
            correction = self.parcouru + (distance_obstacle - self.distance_arret)
            adaptateur.adjust_position(correction)
            self.logger.info(f"[Stop] Arrêt confirmé à {distance_obstacle:.1f}mm (après {self.compteur_detection} cycles)")
            print(f"[Stop] Distance atteinte ({distance_obstacle:.1f} mm), arrêt confirmé")
            return True

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




# Distance (mm) sous laquelle on déclenche l’arrêt d’urgence
DIST_OBS_STOP = 120

class StrategieClavier:
    def __init__(self, adaptateur, key_map):
        self.logger = getLogger(__name__)
        self.adaptateur = adaptateur
        self.key_map = key_map
        self.linear_vel = 0
        self.angular_vel = [0, 0]

    # ------------------------------------------------------------------ #
    def start(self, adaptateur):
        adaptateur.initialise()
        adaptateur.setVitAngA(0)
        adaptateur.tourne(0, 0)
        self.linear_vel = 0
        self.angular_vel = [0, 0]
        self.logger.info("StrategieClavier.start: contrôle par clavier démarré")
        print("Contrôle clavier : i (avancer) | o (reculer) | p (gauche) | l (droite)")

    # ------------------------------------------------------------------ #
    def step(self, adaptateur):
        # 1) Détection proactive d’obstacle --------------------------------
        distance_obs = adaptateur.getDistanceA()      # mm
        if distance_obs < DIST_OBS_STOP:
            self.logger.warning(f"Obstacle à {distance_obs:.0f} mm → arrêt d’urgence")
            self.stop(adaptateur)
            return

        # 2) Collision déjà déclarée ? ------------------------------------
        if adaptateur.estCrash():
            self.stop(adaptateur)
            return

        # 3) Commandes linéaires ------------------------------------------
        if self.key_map.get('i') and not self.key_map.get('o'):
            self.linear_vel = VIT_ANG_AVAN
        elif self.key_map.get('o') and not self.key_map.get('i'):
            self.linear_vel = -VIT_ANG_AVAN
        else:
            self.linear_vel = 0
        adaptateur.setVitAngA(self.linear_vel)

        # 4) Commandes angulaires -----------------------------------------
        if self.key_map.get('p') and not self.key_map.get('l'):
            self.angular_vel = [ VIT_ANG_TOUR, -VIT_ANG_TOUR ]   # gauche
        elif self.key_map.get('l') and not self.key_map.get('p'):
            self.angular_vel = [ -VIT_ANG_TOUR, VIT_ANG_TOUR ]   # droite
        else:
            self.angular_vel = [0, 0]
        adaptateur.tourne(*self.angular_vel)

        # 5) Re-vérification immédiate (au cas où les nouvelles
        #    vitesses provoqueraient une collision dès cette itération)
        if adaptateur.estCrash():
            self.stop(adaptateur)

    # ------------------------------------------------------------------ #
    def stop(self, adaptateur):
        adaptateur.arreter()          # met vitesses moteurs à 0
        self.linear_vel  = 0
        self.angular_vel = [0, 0]
        self.logger.info("StrategieClavier.stop: robot arrêté")
        print("StrategieClavier.stop : robot arrêté – collision ou obstacle détecté")
        return True
