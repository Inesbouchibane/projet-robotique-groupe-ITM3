import math
import random
from robot import Robot
from affichage import Affichage

IR_MAX_DISTANCE = 100
IR_SEUIL_ARRET = 50
LARGEUR, HAUTEUR = 800, 600

class Environnement:
    def __init__(self, vitesse_gauche, vitesse_droite, mode, affichage=True, longueur_carre=200):
        """
        Initialise l'environnement de simulation.
        :param vitesse_gauche: Vitesse de la roue gauche.
        :param vitesse_droite: Vitesse de la roue droite.
        :param mode: "automatique", "manuel" ou "carré".
        :param affichage: True pour affichage graphique, False pour console.
        :param longueur_carre: Longueur du côté du carré (pour le mode carré).
        """
        self.robot = Robot(LARGEUR/2, HAUTEUR/2, vitesse_gauche, vitesse_droite)
        self.mode = mode
        self.obstacles = [
        (200, 200, 100, 100), 
        (400, 100, 50, 50), 
        (600, 270, 50, 50), 
        (700, 500, 80, 80) ]

        self.affichage_active = affichage
        if self.affichage_active:
            self.affichage = Affichage(LARGEUR, HAUTEUR, self.obstacles)
        else:
            self.affichage = None
        self.avoidance_mode = False
        self.avoidance_direction = None
        self.avoidance_counter = 0
        self.default_vg = vitesse_gauche
        self.default_vd = vitesse_droite
        self.segment_length = longueur_carre
        self.trajectoire = []

    def detecter_collision(self, x, y):
        """
        Détecte une collision avec un obstacle.
        """
        for (ox, oy, ow, oh) in self.obstacles:
            if ox < x < ox + ow and oy < y < oy + oh:
                return True
        return False
     

    def detecter_murs(self):
        distances = {
            "haut": self.robot.y,
            "bas": HAUTEUR - self.robot.y,
            "gauche": self.robot.x,
            "droite": LARGEUR - self.robot.x
        }
        return distances


    def demarrer_simulation(self):
        """
        Démarre la simulation.
        En mode "carré", lance directement le tracé du carré.
        En mode "automatique" ou "manuel", exécute la boucle de simulation.
        """
        running = True
        from controleur import Controleur
        controleur = Controleur(self.default_vg, self.default_vd, self.mode, self.affichage_active, self.segment_length, self.robot.x, self.robot.y)
  
        if self.mode == "carré":
            if (self.robot.x - self.segment_length/2 < 0 or self.robot.x + self.segment_length/2 > LARGEUR or
                    self.robot.y - self.segment_length/2 < 0 or self.robot.y + self.segment_length/2 > HAUTEUR):
                print("Position initiale inadaptée pour tracer un carré complet. Recentrage du robot.")
                self.robot.x, self.robot.y = LARGEUR/2, HAUTEUR/2
            controleur.tracer_carre(self.segment_length)
            return

        while running:
            if self.affichage_active:
                action = self.affichage.handle_events()
                if action == "quit":
                    running = False
                    continue
                elif self.mode == "manuel":
                    if action == "stop":
                        self.robot.vitesse_gauche = 0
                        self.robot.vitesse_droite = 0
                        print("Robot arrêté")
                    elif action == "change":
                        if self.robot.vitesse_gauche == 0 and self.robot.vitesse_droite == 0:
                            rep = input("Voulez-vous tracer un carré ? (y/n) : ").strip().lower()
                            # Vider la file d'événements pour éviter des événements résiduels
                            import pygame; pygame.event.clear()
                            if rep == "y":
                                try:
                                    cote = float(input("Entrez la longueur du côté du carré : "))
                    controleur.tracer_carre(cote)
                                except ValueError:
                                    cote = self.segment_length
                                    print(f"Valeur invalide, utilisation de {self.segment_length}.")
                                    controleur.tracer_carre(self.segment_length)

                                continue
                            else:
                                try:
                                    new_vg = float(input("Entrez la nouvelle vitesse de la roue gauche : "))
                                    new_vd = float(input("Entrez la nouvelle vitesse de la roue droite : "))
                                except ValueError:
                                    print("Valeurs invalides. Utilisation des vitesses par défaut (2).")
                                    new_vg, new_vd = 2, 2
                                self.robot.vitesse_gauche = new_vg
                                self.robot.vitesse_droite = new_vd
                                self.default_vg = new_vg
                                self.default_vd = new_vd
                                print("Robot démarré avec nouvelles vitesses")
                    elif action == "reset":
                        self.robot.x, self.robot.y = LARGEUR/2, HAUTEUR/2
                        if self.affichage_active:
                            self.affichage.reset_trajet()
                        print("Robot réinitialisé")

            old_x, old_y = self.robot.x, self.robot.y
            self.robot.deplacer()
            if self.detecter_collision(self.robot.x, self.robot.y):
                self.robot.x, self.robot.y = old_x, old_y

            ir_point = self.robot.scan_infrarouge(self.obstacles, IR_MAX_DISTANCE)
            distance_ir = math.hypot(ir_point[0] - self.robot.x, ir_point[1] - self.robot.y)

        if self.mode == "automatique":
                if distance_ir < IR_SEUIL_ARRET or self.detecter_collision(self.robot.x, self.robot.y):
                    if not self.avoidance_mode:
                        self.robot.angle = random.uniform(0, 360)
                        self.avoidance_mode = True
                        self.avoidance_counter = 30
                        print(f"Obstacle détecté à {distance_ir:.2f}px ! Nouvelle direction: {self.robot.angle:.2f}°")
                    else:
                        if self.avoidance_counter > 0:
                            self.avoidance_counter -= 1
                    self.robot.vitesse_gauche = self.default_vg
                    self.robot.vitesse_droite = self.default_vd
                else:
                    if self.avoidance_mode and self.avoidance_counter == 0:
                        self.avoidance_mode = False
                        self.robot.vitesse_gauche = self.default_vg
                        self.robot.vitesse_droite = self.default_vd

            if self.affichage_active:
                self.affichage.mettre_a_jour(self.robot, ir_point, distance_ir)
            else:
                print(f"Position: ({self.robot.x:.2f}, {self.robot.y:.2f}) - Distance IR: {distance_ir:.2f}")
