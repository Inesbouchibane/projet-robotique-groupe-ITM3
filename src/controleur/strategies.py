import math as m
from src.utils import VIT_ANG_AVAN, VIT_ANG_TOUR, getDistanceFromPts, contientBalise
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
        if adaptateur.estCrash():
            print("Collision détectée, arrêt.")
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
        StrategieTourner(90),
        StrategieAvancer(longueur_cote),
        StrategieTourner(90),
        StrategieAvancer(longueur_cote),
        StrategieTourner(90),
        StrategieAvancer(longueur_cote),
        StrategieTourner(90)
    ])
 


class StrategieArretMur:
    VIT_ANG_AVAN = 20# Default angular speed in deg/s

    def __init__(self, adaptateur, distance_arret):
        """Stratégie pour avancer jusqu'à une distance donnée d'un mur
        :param adaptateur: Adaptateur du robot
        :param distance_arret: Distance minimale à maintenir du mur (mm)
        """
        self.logger = getLogger(__name__)
        self.adaptateur = adaptateur
        self.distance_arret = distance_arret

    def start(self, adaptateur):
        adaptateur.initialise()
        vitesse_max = self.VIT_ANG_AVAN  # Use class constant
        adaptateur.setVitAngA(vitesse_max)
        self.logger.info(f"StrategieArretMur.start : vitesse={vitesse_max}, distance_arret={self.distance_arret}mm")

    def step(self, adaptateur):
        distance_obstacle = adaptateur.getDistanceA()
        self.logger.debug(f"StrategieArretMur.step : distance_obstacle={distance_obstacle:.2f}mm")
        # Vérifier si la distance est valide
        if distance_obstacle is None or distance_obstacle < 0:
            self.logger.warning("Distance à l'obstacle invalide, continue à avancer")
            adaptateur.setVitAngA(self.VIT_ANG_AVAN)
            return
        # Continuer à avancer si pas à la distance cible
        if not self.stop(adaptateur):
            adaptateur.setVitAngA(self.VIT_ANG_AVAN)

    def stop(self, adaptateur):
        distance_obstacle = adaptateur.getDistanceA()
        if adaptateur.estCrash():
            adaptateur.setVitAngA(0)
            self.logger.info("StrategieArretMur.stop : collision détectée, arrêt")
            print("StrategieArretMur.stop : collision détectée, arrêt")
            return True
        if distance_obstacle is None or distance_obstacle < 0:
            self.logger.warning("Distance à l'obstacle invalide, continue")
            return False
        if distance_obstacle <= self.distance_arret:
            adaptateur.setVitAngA(0)
            self.logger.info(f"StrategieArretMur.stop : distance_arret atteinte ({distance_obstacle:.2f}mm), arrêt")
            print(f"StrategieArretMur.stop : distance_arret atteinte ({distance_obstacle:.2f}mm), arrêt")
            return True
        self.logger.debug("StrategieArretMur.stop : continue")
        return False

class StrategieSuivreBalise:
    def __init__(self, adaptateur):
        """Stratégie permettant au robot de suivre une balise
        :param adaptateur: Adaptateur du robot
        """
        self.logger = getLogger(self.__class__.__name__)
        self.adaptateur = adaptateur
        self.cptfalse = 0
        self.balise = False
        self.decale = 0

    def start(self, adaptateur):
        """Réinitialisation du robot, du décalage et de balise"""
        self.adaptateur.robot.estSousControle = True
        self.balise, self.decale = contientBalise(self.adaptateur.get_imageA())
        self.cptfalse = 0
        self.logger.debug("Stratégie Suivre Balise lancée")

    def step(self, adaptateur):
        """Met à jour le décalage et ajuste la vitesse des roues en fonction du décalage"""
        if not self.stop(adaptateur):
            self.balise, self.decale = contientBalise(self.adaptateur.get_imageA())
            print(f"Balise détectée: {self.balise}, décalage: {self.decale}")
            if self.balise:
                self.adaptateur.setVitAngA(1)
                if self.decale > 100:
                    self.adaptateur.setVitAngG(2)
                    self.adaptateur.setVitAngD(1)
                elif self.decale < -100:
                    self.adaptateur.setVitAngG(1)
                    self.adaptateur.setVitAngD(2)
                else:
                    self.adaptateur.setVitAngG(1)
                    self.adaptateur.setVitAngD(1)
                self.cptfalse = 0
            else:
                self.adaptateur.setVitAng(0)
                self.cptfalse += 1

    def stop(self, adaptateur):
        """Retourne True si la balise n'est plus détectée après 100 tentatives ou si collision"""
        if adaptateur.estCrash():
            self.adaptateur.setVitAngA(0)
            self.adaptateur.robot.estSousControle = False
            self.logger.info("Arrêt: collision détectée")
            return True
        if self.cptfalse > 100:
            self.adaptateur.setVitAngA(0)
            self.adaptateur.robot.estSousControle = False
            self.logger.info("Balise non détectée après 100 tentatives, arrêt")
            return True
        return False