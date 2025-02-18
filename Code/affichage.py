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



class Affichage:
    def __init__(self, largeur, hauteur, obstacles):
        """
        Initialise l'affichage de la simulation.
        :param largeur: Largeur de la fenêtre.
        :param hauteur: Hauteur de la fenêtre.
        :param obstacles: Liste des obstacles.
        """
        pygame.init()
        self.ecran = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Simulation Robot")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.obstacles = obstacles
        self.trajet = []
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
        Met à jour l'affichage de la simulation.
        :param robot: Instance du robot.
        :param ir_point: Point détecté par le capteur infrarouge.
        :param distance_ir: Distance détectée par le capteur.
        """
        self.ecran.fill(BLANC)
        self.trajet.append((robot.x, robot.y))
        if len(self.trajet) > 1:
            pygame.draw.lines(self.ecran, NOIR, False, self.trajet, 2)

        for( ox, oy, ow, oh) in self.obstacles:
            pygame.draw.rect(self.ecran, ROUGE, (ox, oy, ow, oh))
        
        pygame.draw.polygon(self.ecran, BLEU, self.calculer_points_robot(robot))
        pygame.draw.line(self.ecran, VERT, (robot.x, robot.y), ir_point, 2)
        pygame.draw.circle(self.ecran, MAGENTA, (int(ir_point[0]), int(ir_point[1])), 5)
        
        text = self.font.render(f"Distance: {round(distance_ir,2)} px", True, NOIR)
        self.ecran.blit(text, (10, 10))
        
        pygame.display.flip()
        self.clock.tick(30)

    def reset_trajet(self):
        """
        Réinitialise la trajectoire du robot.
        """
        self.trajet = []

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

    
