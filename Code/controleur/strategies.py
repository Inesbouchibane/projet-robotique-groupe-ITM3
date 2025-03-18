from logging import getLogger

class StrategieAvancer:
    def __init__(self, robAdapt, distance):
        self.logger = getLogger(self.__class__.__name__)
        self.distance = distance
        self.robA = robAdapt
        self.parcouru = 0
        self.robA.initialise()

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
        self.angle = angle
        self.angle_parcouru = 0
        self.robA.initialise()

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
