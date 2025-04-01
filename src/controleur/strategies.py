import math as m
from src.utils import VIT_ANG_AVAN, VIT_ANG_TOUR, getDistanceFromPts
from math import atan2, degrees, cos, sin

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
        self.angle_cible = m.radians(angle)  # Convert to radians
        self.angle_parcouru = 0

    def start(self, adaptateur):
        adaptateur.initialise()
        self.angle_parcouru = 0
        if self.angle_cible > 0:  # Turn left
            adaptateur.setVitAngGA(-VIT_ANG_TOUR)
            adaptateur.setVitAngDA(VIT_ANG_TOUR)
        else:  # Turn right
            adaptateur.setVitAngGA(VIT_ANG_TOUR)
            adaptateur.setVitAngDA(-VIT_ANG_TOUR)
        print(f"Début de la rotation, cible: {m.degrees(self.angle_cible)} degrés")

    def step(self, adaptateur):
        self.angle_parcouru = adaptateur.getAngleParcouru()
        position = adaptateur.getPosition()
        direction = m.degrees(m.atan2(adaptateur.getDirection()[1], adaptateur.getDirection()[0]))
        print(f"Position: {position}, Direction: {direction:.2f}°, Angle parcouru: {m.degrees(self.angle_parcouru):.2f}/{m.degrees(self.angle_cible)} degrés")

    def stop(self, adaptateur):
        if adaptateur.getDistanceObstacle() < 20:
            print("Obstacle détecté, arrêt.")
            adaptateur.setVitAngGA(0)
            adaptateur.setVitAngDA(0)
            return True
        if abs(self.angle_parcouru) >= abs(self.angle_cible) - 0.01:  # Small tolerance
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
        adaptateur.setVitAngGA(self.vitAngG)
        adaptateur.setVitAngDA(self.vitAngD)
        print(f"Début de la stratégie auto avec vitAngG={self.vitAngG}, vitAngD={self.vitAngD}")

    def step(self, adaptateur):
        adaptateur.setVitAngGA(self.vitAngG)
        adaptateur.setVitAngDA(self.vitAngD)
        print(f"Step - Envoi : vitAngG={self.vitAngG}, vitAngD={self.vitAngD}, Après : G={adaptateur.getVitG()}, D={adaptateur.getVitD()}")

    def stop(self, adaptateur):
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



class StrategieSuivreBalise:
    def __init__(self, balise_position, distance_securite=20, vitesse_max=VIT_ANG_AVAN, tolerance_angle=5):
        """
        Initialise la stratégie pour suivre une balise.
        :param balise_position: Tuple (x, y) représentant la position de la balise
        :param distance_securite: Distance minimale à maintenir avec les obstacles (en unités)
        :param vitesse_max: Vitesse angulaire maximale pour avancer
        :param tolerance_angle: Tolérance en degrés pour considérer l'alignement correct
        """
        self.balise_position = balise_position  # Position cible (x, y)
        self.distance_securite = distance_securite
        self.vitesse_max = vitesse_max
        self.tolerance_angle = tolerance_angle  # Tolérance en degrés pour l'alignement
        self.distance_parcourue = 0

    def start(self, adaptateur):
        """Démarre la stratégie."""
        adaptateur.initialise()
        self.distance_parcourue = 0
        print(f"Début de la stratégie Suivre Balise vers {self.balise_position}")

    def step(self, adaptateur):
        """Exécute une étape de la stratégie."""
        # Récupérer la position et la direction actuelle du robot
        position_robot = adaptateur.getPosition()  # (x, y)
        direction_robot = adaptateur.getDirection()  # Vecteur [cos, sin]
        distance_obstacle = adaptateur.getDistanceObstacle()  # Distance à l'obstacle le plus proche

        # Calculer l'angle vers la balise
        dx = self.balise_position[0] - position_robot[0]
        dy = self.balise_position[1] - position_robot[1]
        angle_cible = atan2(dy, dx)  # Angle en radians vers la balise
        angle_robot = atan2(direction_robot[1], direction_robot[0])  # Angle actuel du robot
        angle_diff = self.normalize_angle(angle_cible - angle_robot)  # Différence d'angle

        # Calculer la distance à la balise
        distance_balise = getDistanceFromPts(position_robot, self.balise_position)

        # Afficher les informations
        print(f"Position: {position_robot}, Direction: {degrees(angle_robot):.2f}°, "
              f"Angle vers balise: {degrees(angle_cible):.2f}°, Distance à balise: {distance_balise:.2f}")

        # Si un obstacle est trop proche, arrêter
        if distance_obstacle < self.distance_securite:
            print("Obstacle trop proche, arrêt temporaire.")
            adaptateur.setVitAngGA(0)
            adaptateur.setVitAngDA(0)
            return

        # Ajuster la direction si l'angle est trop grand
        if abs(degrees(angle_diff)) > self.tolerance_angle:
            # Tourner vers la balise
            vitesse_tour = min(VIT_ANG_TOUR, abs(angle_diff) * 0.5)  # Ajustement proportionnel
            if angle_diff > 0:  # Tourner à gauche
                adaptateur.setVitAngGA(-vitesse_tour)
                adaptateur.setVitAngDA(vitesse_tour)
            else:  # Tourner à droite
                adaptateur.setVitAngGA(vitesse_tour)
                adaptateur.setVitAngDA(-vitesse_tour)
            print(f"Ajustement direction: Angle diff = {degrees(angle_diff):.2f}°")
        else:
            # Avancer vers la balise si aligné
            vitesse = min(self.vitesse_max, distance_balise * 0.1)  # Vitesse proportionnelle à la distance
            adaptateur.setVitAngGA(vitesse)
            adaptateur.setVitAngDA(vitesse)
            print(f"Avancer vers balise avec vitesse: {vitesse:.2f}")

        # Mettre à jour la distance parcourue
        self.distance_parcourue = adaptateur.getDistanceParcourue()

    def stop(self, adaptateur):
        """Condition d'arrêt de la stratégie."""
        position_robot = adaptateur.getPosition()
        distance_balise = getDistanceFromPts(position_robot, self.balise_position)
        distance_obstacle = adaptateur.getDistanceObstacle()

        # Arrêt si trop proche d'un obstacle
        if distance_obstacle < self.distance_securite:
            print("Obstacle détecté, arrêt définitif.")
            adaptateur.setVitAngGA(0)
            adaptateur.setVitAngDA(0)
            return True

        # Arrêt si la balise est atteinte (distance < 5 unités)
        if distance_balise < 5:
            print("Balise atteinte, arrêt.")
            adaptateur.setVitAngGA(0)
            adaptateur.setVitAngDA(0)
            return True

        return False

    def normalize_angle(self, angle):
        """Normalise un angle entre -π et π."""
        while angle > m.pi:
            angle -= 2 * m.pi
        while angle < -m.pi:
            angle += 2 * m.pi
        return angle
