import pygame
import math

# Définition des couleurs et dimensions
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
JAUNE = (255, 255, 0)

class Affichage:
    def __init__(self, largeur, hauteur, obstacles):
        """
        Initialise l'affichage graphique.
        :param largeur: Largeur de la fenêtre.
        :param hauteur: Hauteur de la fenêtre.
        :param obstacles: Liste des obstacles à dessiner.
        """
        pygame.init()
        self.ecran = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Simulation Robot")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.obstacles = obstacles
        self.trajet = []
	self.distance_totale = 0 
	self.robot_arrete = False  # Pour suivre si le robot est arrêté


    def handle_events(self):
        """
        Gère les événements Pygame et renvoie une action.
        :return: Une chaîne ("quit", "stop", "change", "reset") ou None.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return "stop"
                elif event.key == pygame.K_d:
                    return "change"
                elif event.key == pygame.K_r:
                    return "reset"
        return None

    def mettre_a_jour(self, robot, ir_point, distance_ir):
        """
        Met à jour l'affichage : efface l'écran, dessine la trajectoire, les obstacles,
        le robot et la ligne du capteur.
        :param robot: Instance du robot.
        :param ir_point: Point détecté par le capteur infrarouge.
        :param distance_ir: Distance mesurée par le capteur.
        """
	if len(self.trajet) > 0:
    	    last_point = self.trajet[-1]
    	    delta_dist = math.hypot(robot.x - last_point[0], robot.y - last_point[1])
    	    self.distance_totale += delta_dist

	self.ecran.fill(BLANC)

	self.trajet.append((robot.x, robot.y))
        if len(self.trajet) > 1:
            pygame.draw.lines(self.ecran, NOIR, False, self.trajet, 2)

        for (ox, oy, ow, oh) in self.obstacles:
            pygame.draw.rect(self.ecran, ROUGE, (ox, oy, ow, oh))

	couleur_robot = JAUNE if self.robot_arrete else BLEU
	pygame.draw.polygon(self.ecran, couleur_robot, self.calculer_points_robot(robot))

	if ir_point:
            pygame.draw.line(self.ecran, VERT, (robot.x, robot.y), ir_point, 2)
            pygame.draw.circle(self.ecran, MAGENTA, (int(ir_point[0]), int(ir_point[1])), 5)
	
	# Afficher la distance IR en haut de la fenêtre
        text_ir = self.font.render(f"Distance IR: {round(distance_ir, 2)} px", True, NOIR)
        self.ecran.blit(text_ir, (10, 10))  # Position du texte en haut à gauche

        if self.robot_arrete:
            text_arret = self.font.render("Robot arrêté (obstacle détecté)", True, NOIR)
            self.ecran.blit(text_arret, (10, 40))  # Position du texte en dessous de la distance IR

	# Afficher la distance totale parcourue
        text_total = self.font.render(f"Distance parcourue: {round(self.distance_totale, 2)} px", True, NOIR)
        self.ecran.blit(text_total, (10, 70))  # Position du texte en dessous du message d'arrêt


        # Mettre à jour l'affichage
        pygame.display.flip()
        self.clock.tick(60)

    def reset_trajet(self):
        """Réinitialise la trajectoire enregistrée."""
        self.trajet = []
	self.distance_totale = 0

    def calculer_points_robot(self, robot):
        """
        Calcule les points du polygone représentant le robot.
        :param robot: Instance du robot.
        :return: Liste des points du polygone.
        """
        cos_a = math.cos(math.radians(robot.angle))
        sin_a = math.sin(math.radians(robot.angle))
        return [
            (robot.x + cos_a * robot.longueur / 2 - sin_a * robot.largeur / 2,
             robot.y - sin_a * robot.longueur / 2 - cos_a * robot.largeur / 2),
            (robot.x - cos_a * robot.longueur / 2 - sin_a * robot.largeur / 2,
             robot.y + sin_a * robot.longueur / 2 - cos_a * robot.largeur / 2),
            (robot.x - cos_a * robot.longueur / 2 + sin_a * robot.largeur / 2,
             robot.y + sin_a * robot.longueur / 2 + cos_a * robot.largeur / 2),
            (robot.x + cos_a * robot.longueur / 2 + sin_a * robot.largeur / 2,
             robot.y - sin_a * robot.longueur / 2 + cos_a * robot.largeur / 2)
        ]
     def attendre_fermeture(self):
        """

        Attend que l'utilisateur ferme la fenêtre ou appuie sur une touche pour quitter.
        """
        print("Appuyez sur une touche pour quitter...")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return

    def __del__(self):
        pygame.quit()
