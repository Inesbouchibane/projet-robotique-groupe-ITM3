import logging
from environnement import Environnement

class Controleur:
    def __init__(self, vitesse_gauche, vitesse_droite, mode, affichage=True, longueur_carre=200):
        """
        Initialise le contrôleur avec les paramètres de simulation.
        :param vitesse_gauche: Vitesse de la roue gauche.
        :param vitesse_droite: Vitesse de la roue droite.
        :param mode: "automatique", "manuel" ou "carré".
        :param affichage: True pour affichage graphique, False pour console.
        :param longueur_carre: Longueur du côté du carré (pour le mode carré).
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.env = Environnement(vitesse_gauche, vitesse_droite, mode, affichage, longueur_carre)
        self.logger.info("Contrôleur initialisé en mode: %s", mode)

        def avancer(self, distance):
        self.logger.info("Début avancement de %.2f unités, position: (%.2f, %.2f), angle: %.2f", 
                         distance, self.env.robot.x, self.env.robot.y, self.env.robot.angle)
        distance_parcourue = 0
        max_iterations = 1000
        iteration = 0

        while distance_parcourue < distance and iteration < max_iterations:
            ir_point = self.env.robot.scan_infrarouge(self.env.obstacles, self.env.IR_MAX_DISTANCE)
            distance_ir = math.hypot(ir_point[0] - self.env.robot.x, ir_point[1] - self.env.robot.y)
            if distance_ir < 50 or self.env.detecter_collision(self.env.robot.x, self.env.robot.y):
                self.logger.warning("Obstacle détecté pendant l'avancement (distance IR: %.2f)", distance_ir)
                print("Obstacle détecté ! Arrêt de l'avancement.")
                self.env.robot.vitesse_gauche = 0
                self.env.robot.vitesse_droite = 0
                return False  # Arrêt de l'avancement

            self.env.robot.vitesse_gauche = self.vitesse_gauche_initiale
            self.env.robot.vitesse_droite = self.vitesse_droite_initiale
            old_x, old_y = self.env.robot.x, self.env.robot.y
            self.env.robot.deplacer()
            distance_parcourue += self.env.robot.distance_parcourue()

            if self.env.affichage_active and iteration % 10 == 0:
                # Mise à jour avec le point IR réel pour garder l'affichage du capteur
                ir_point = self.env.robot.scan_infrarouge(self.env.obstacles, self.env.IR_MAX_DISTANCE)
                distance_ir = math.hypot(ir_point[0] - self.env.robot.x, ir_point[1] - self.env.robot.y)
                self.env.affichage.mettre_a_jour(self.env.robot, ir_point, distance_ir)
                pygame.time.delay(10)  # Délai réduit pour un mouvement plus fluide
            iteration += 1

        self.logger.info("Avancement terminé, distance parcourue: %.2f, position: (%.2f, %.2f)", 
                         distance_parcourue, self.env.robot.x, self.env.robot.y)
        return True  # Avancement réussi


    def demarrer_simulation(self):
        """
        Le contrôleur lance la simulation en appelant la méthode
        demarrer_simulation de l'environnement.
        """
        self.logger.info("Démarrage de la simulation...")
        self.env.demarrer_simulation()
        self.logger.info("Simulation terminée.")

    def ajuster_vitesse(self, vitesse_gauche, vitesse_droite):
        """
        Permet d'ajuster les vitesses du robot en cours de simulation.
        """
        self.env.robot.vitesse_gauche = vitesse_gauche
        self.env.robot.vitesse_droite = vitesse_droite
        self.logger.info("Vitesses ajustées: vg=%.2f, vd=%.2f", vitesse_gauche, vitesse_droite)
    
    def tourner(self, angle):
        self.logger.info("Rotation de %d degrés, angle actuel: %.2f", angle, self.env.robot.angle)
        current_angle = self.env.robot.angle
        target_angle = (current_angle + angle) % 360
        rotation_precision = 1.0
        max_iterations = 1000
        iteration = 0

        while abs((self.env.robot.angle - target_angle + 360) % 360) > rotation_precision and iteration < max_iterations:
            delta = (target_angle - self.env.robot.angle + 360) % 360
            direction = 1 if delta < 180 else -1
            vitesse_rotation = 1.5
            self.env.robot.vitesse_gauche = direction * vitesse_rotation
            self.env.robot.vitesse_droite = -direction * vitesse_rotation
            old_x, old_y = self.env.robot.x, self.env.robot.y
            self.env.robot.deplacer()

            ir_point = self.env.robot.scan_infrarouge(self.env.obstacles, self.env.IR_MAX_DISTANCE)
            distance_ir = math.hypot(ir_point[0] - self.env.robot.x, ir_point[1] - self.env.robot.y)
            if distance_ir < 50 or self.env.detecter_collision(self.env.robot.x, self.env.robot.y):
                self.env.robot.x, self.env.robot.y = old_x, old_y
                self.logger.warning("Obstacle détecté pendant la rotation (distance IR: %.2f)", distance_ir)
                print("Obstacle détecté pendant la rotation ! Arrêt.")
                self.env.robot.vitesse_gauche = 0
                self.env.robot.vitesse_droite = 0
                return False  # Arrêt de la rotation

            if self.env.affichage_active and iteration % 10 == 0:
                self.env.affichage.mettre_a_jour(self.env.robot, ir_point, distance_ir)
            iteration += 1

        self.logger.info("Rotation terminée, angle atteint: %.2f (cible: %.2f)", self.env.robot.angle, target_angle)
        return True  
