# src/interface_graphique/interface2D/affichage.py

import pygame
from src.utils import getDistanceFromPts
from logging import getLogger

logger = getLogger(__name__)

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
JAUNE = (255, 255, 0)

class Affichage:
    def __init__(self, largeur, hauteur, obstacles_points):
        pygame.init()
        self.ecran = pygame.display.set_mode((largeur, hauteur))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.obstacles_points = obstacles_points
        self.trajet = []
        self.last_position = None

    def bleu(self):
        self.couleur_trace = (0, 0, 255)  # Bleu

    def rouge(self):
        self.couleur_trace = (255, 0, 0)  # Rouge

    def dessine(self, b):
        self.dessine_trace = b

    def move(self, dx, dy):
        if self.dessine_trace:
            pygame.draw.line(self.screen, self.couleur_trace, (self.x, self.y), (self.x + dx, self.y + dy), 2)
        self.x += dx
        self.y += dy




    def mettre_a_jour(self, robot):
        self.ecran.fill(BLANC)
        current_position = (robot.x, robot.y)
        if self.last_position is None or getDistanceFromPts(current_position, self.last_position) > 1:
            self.trajet.append(current_position)
            self.last_position = current_position
        if len(self.trajet) > 1:
            pygame.draw.lines(self.ecran, NOIR, False, self.trajet, 2)

        for points in self.obstacles_points:
            pygame.draw.polygon(self.ecran, ROUGE, points)

        points = self.calculer_points_robot(robot)
        pygame.draw.polygon(self.ecran, JAUNE if robot.estCrash else BLEU, points)
        pos_text = self.font.render(f"Pos: ({robot.x:.1f}, {robot.y:.1f})", True, NOIR)
        self.ecran.blit(pos_text, (10, 10))
        pygame.display.flip()

    def calculer_points_robot(self, robot):
        cos_a, sin_a = robot.direction[0], robot.direction[1]
        return [
            (robot.x + cos_a * robot.length / 2 - sin_a * robot.width / 2,
             robot.y + sin_a * robot.length / 2 + cos_a * robot.width / 2),
            (robot.x - cos_a * robot.length / 2 - sin_a * robot.width / 2,
             robot.y - sin_a * robot.length / 2 + cos_a * robot.width / 2),
            (robot.x - cos_a * robot.length / 2 + sin_a * robot.width / 2,
             robot.y - sin_a * robot.length / 2 - cos_a * robot.width / 2),
            (robot.x + cos_a * robot.length / 2 + sin_a * robot.width / 2,
             robot.y + sin_a * robot.length / 2 - cos_a * robot.width / 2)
        ]

    def attendre_fermeture(self):
        pygame.quit()