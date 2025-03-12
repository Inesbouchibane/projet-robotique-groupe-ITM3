import logging
import math
import time
from environnement import Environnement

class Controleur:
    def __init__(self, vitesse_gauche, vitesse_droite, mode, affichage=True, longueur_carre=200, pos_x=400, pos_y=300):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        self.env = Environnement(vitesse_gauche, vitesse_droite, mode, affichage, longueur_carre, pos_x, pos_y)
        self.logger.info("Contrôleur initialisé en mode: %s", mode)
        self.vitesse_gauche_initiale = vitesse_gauche  # Stocker la vitesse initiale
        self.vitesse_droite_initiale = vitesse_droite  # Stocker la vitesse initiale

    def ajuster_vitesse(self, vitesse_gauche, vitesse_droite):
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

            # Correction pour tourner correctement vers la gauche
            if angle > 0:  # Si l'angle est positif, on tourne à gauche
                self.env.robot.vitesse_gauche = -direction * vitesse_rotation
                self.env.robot.vitesse_droite = direction * vitesse_rotation
            else:  # Sinon, on tourne à droite
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
        return True  # Rotation réussie

    def tourner_instant(self, angle):
        """
        Effectue une rotation instantanée (utilisée pour le mode carré).
        """
        self.env.robot.angle = (self.env.robot.angle + angle) % 360
        if self.env.affichage_active:
            ir_point = self.env.robot.scan_infrarouge(self.env.obstacles, self.env.IR_MAX_DISTANCE)
            self.env.affichage.mettre_a_jour(
                self.env.robot,
                ir_point,
                math.hypot(ir_point[0] - self.env.robot.x, ir_point[1] - self.env.robot.y)
            )
        self.logger.info("Rotation instantanée de %d degrés, nouvel angle: %.2f", angle, self.env.robot.angle)

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
                ir_point = self.env.robot.scan_infrarouge(self.env.obstacles, self.env.IR_MAX_DISTANCE)
                distance_ir = math.hypot(ir_point[0] - self.env.robot.x, ir_point[1] - self.env.robot.y)
                self.env.affichage.mettre_a_jour(self.env.robot, ir_point, distance_ir)

            time.sleep(0.01)  # Délai réduit pour un mouvement plus fluide
            iteration += 1

        self.logger.info("Avancement terminé, distance parcourue: %.2f, position: (%.2f, %.2f)",
                         distance_parcourue, self.env.robot.x, self.env.robot.y)
        return True  # Avancement réussi

    def avancer_vers_mur_proche(self):
        """
        Détermine le mur le plus proche et avance vers lui tout en évitant les obstacles.
        Affiche des messages clairs pour indiquer le mur le plus proche et l'avancement.
        La fenêtre reste ouverte jusqu'à ce que l'utilisateur la ferme manuellement.
        """
        # Détecter les distances aux murs
        distances = self.env.detecter_murs()
        mur_proche = min(distances, key=distances.get)
        distance_mur = distances[mur_proche]

        # Afficher le mur le plus proche
        print(f"Mur le plus proche détecté : {mur_proche} à une distance de {distance_mur:.2f} px")

        # Calculer l'angle nécessaire pour se diriger vers le mur le plus proche
        if mur_proche == "haut":
            angle_cible = 270  # Le robot doit pointer vers le haut (angle 270°)
        elif mur_proche == "bas":
            angle_cible = 90   # Le robot doit pointer vers le bas (angle 90°)
        elif mur_proche == "gauche":
            angle_cible = 180  # Le robot doit pointer vers la gauche (angle 180°)
        elif mur_proche == "droite":
            angle_cible = 0    # Le robot doit pointer vers la droite (angle 0°)
        else:
            print("Erreur : Mur non reconnu")
            return

        # Calculer la rotation la plus courte
        delta_angle = (angle_cible - self.env.robot.angle + 360) % 360
        if delta_angle > 180:
            delta_angle -= 360  # Tourner dans l'autre sens si c'est plus court
            
        #Correction des angles
        if mur_proche == "haut":
            delta_angle = (delta_angle + 180) % 360 
        elif mur_proche == "bas":
            delta_angle = (delta_angle + 180) % 360
              
        # Afficher l'angle cible et la rotation nécessaire
        print(f"Orientation du robot vers le mur : angle cible = {angle_cible}°")
        print(f"Rotation nécessaire : {delta_angle}°")

        # Tourner vers le mur le plus proche
        if not self.tourner(delta_angle):
            print("Rotation interrompue à cause d'un obstacle.")
            return

        # Avancer vers le mur tout en vérifiant les obstacles
        print("Début de l'avancement vers le mur...")
        while distance_mur > 10:  # On s'arrête à 10 px du mur pour éviter une collision
            # Mettre à jour la distance au mur
            distances = self.env.detecter_murs()
            if mur_proche not in distances:
                print(f"Erreur: Le mur le plus proche '{mur_proche}' n'est plus détecté.")
                break
            distance_mur = distances[mur_proche]
            print(f"Distance actuelle au mur : {distance_mur:.2f} px")

            # Avancer d'un petit pas (par exemple, 10 px)
            if not self.avancer(10):  # Si un obstacle est détecté, arrêter
                print("Obstacle détecté ! Arrêt de l'avancement.")
                break

            # Mettre à jour l'affichage graphique (si activé)
            if self.env.affichage_active:
                ir_point = self.env.robot.scan_infrarouge(self.env.obstacles, self.env.IR_MAX_DISTANCE)
                distance_ir = math.hypot(ir_point[0] - self.env.robot.x, ir_point[1] - self.env.robot.y)
                self.env.affichage.mettre_a_jour(self.env.robot, ir_point, distance_ir)

            time.sleep(0.1)  # Petit délai pour rendre l'affichage fluide

        print("Le robot a atteint le mur ou a été arrêté par un obstacle.")
        # Garder la fenêtre ouverte jusqu'à ce que l'utilisateur la ferme
        if self.env.affichage_active:
            self.env.affichage.attendre_fermeture()

    def tracer_carre(self, cote):
        """
        Fait tracer un carré de côté donné par le robot avec les vitesses initiales.
        Avant de commencer, vérifie que la trajectoire du carré reste dans les limites.
        Utilise une rotation instantanée pour éviter les délais entre chaque côté.
        Vérifie également les collisions avec les obstacles.
        """
        # Vérifier si la position initiale permet de tracer un carré complet
        x, y = self.env.robot.x, self.env.robot.y
        if (x - cote/2 < 0 or x + cote/2 > 800 or y - cote/2 < 0 or y + cote/2 > 600):
            self.logger.warning("Position initiale inadaptée pour un carré de côté %.2f. Recentrage du robot.", cote)
            self.env.robot.x, self.env.robot.y = 400, 300
            print(f"Tracé d'un carré de côté {cote}, position initiale: ({self.env.robot.x}, {self.env.robot.y})")

        if self.env.affichage_active:
            self.env.affichage.reset_trajet()

        # Tracer les 4 côtés
        for i in range(4):
            distance_parcourue = 0
            while distance_parcourue < cote:
                old_x, old_y = self.env.robot.x, self.env.robot.y
                self.env.robot.vitesse_gauche = self.vitesse_gauche_initiale
                self.env.robot.vitesse_droite = self.vitesse_droite_initiale
                self.env.robot.deplacer()
                delta_dist = math.hypot(self.env.robot.x - old_x, self.env.robot.y - old_y)
                distance_parcourue += delta_dist

                # Vérifier les limites
                if not (0 <= self.env.robot.x <= 800 and 0 <= self.env.robot.y <= 600):
                    self.logger.warning("Le robot a atteint les limites pendant le tracé du carré. Arrêt.")
                    self.env.robot.x, self.env.robot.y = old_x, old_y
                    self.env.robot.vitesse_gauche = 0
                    self.env.robot.vitesse_droite = 0
                    break  # Arrêter ce côté du carré

                # Vérifier si une collision avec un obstacle se produit
                if self.env.detecter_collision(self.env.robot.x, self.env.robot.y):
                    self.logger.warning("Collision détectée avec un obstacle pendant le tracé du carré. Arrêt.")
                    self.env.robot.x, self.env.robot.y = old_x, old_y
                    self.env.robot.vitesse_gauche = 0
                    self.env.robot.vitesse_droite = 0
                    break  # Arrêter ce côté du carré

                # Vérifier la distance IR pour éviter de frôler les obstacles
                ir_point = self.env.robot.scan_infrarouge(self.env.obstacles, self.env.IR_SEUIL_ARRET)
                distance_ir = math.hypot(ir_point[0] - self.env.robot.x, ir_point[1] - self.env.robot.y)
                if distance_ir < self.env.IR_SEUIL_ARRET:
                    self.logger.warning("Obstacle détecté à proximité pendant le tracé du carré. Arrêt.")
                    self.env.robot.x, self.env.robot.y = old_x, old_y
                    self.env.robot.vitesse_gauche = 0
                    self.env.robot.vitesse_droite = 0
                    break  # Arrêter ce côté du carré

                if self.env.affichage_active:
                    self.env.affichage.mettre_a_jour(self.env.robot, ir_point, distance_ir)

                time.sleep(0.01)  # Délai réduit pour plus de réactivité

            # Si le robot s'est arrêté à cause d'un obstacle, on quitte la boucle
            if self.env.robot.vitesse_gauche == 0 and self.env.robot.vitesse_droite == 0:
                break  # Arrêter le tracé du carré

            # Rotation instantanée pour passer directement au côté suivant
            self.tourner_instant(90)

            self.env.robot.vitesse_gauche = 0
            self.env.robot.vitesse_droite = 0

        print("Carré terminé ou arrêté à cause d'un obstacle")

        # Garder la fenêtre ouverte après l'arrêt du robot
        if self.env.affichage_active:
            print("Appuyez sur Entrée pour quitter...")
            input()

    def executer_strategies(self, strategies):
        self.logger.info("Exécution de %d stratégies", len(strategies))
        for strategie, args in strategies:
            strategie(**args)
        self.logger.info("Stratégies exécutées avec succès")
