import pygame
from utils import getDistanceFromPts
from logging import getLogger

logger = getLogger(__name__)

BLANC, NOIR, BLEU, ROUGE, JAUNE = (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0)

class Affichage:
    def __init__(self, largeur, hauteur, obstacles):
        pygame.init()
        self.ecran = pygame.display.set_mode((largeur, hauteur))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.obstacles = obstacles
        self.trajet = []
        self.last_position = None

    def handle_events(self, adaptateur):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                return "tracer_carre"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                return "automatique"
        return None

    def mettre_a_jour(self, robot):
        self.ecran.fill(BLANC)
        current_position = (robot.x, robot.y)
        if self.last_position is None or getDistanceFromPts(current_position, self.last_position) > 1:
            self.trajet.append(current_position)
            self.last_position = current_position

        if len(self.trajet) > 1:
            pygame.draw.lines(self.ecran, NOIR, False, self.trajet, 2)

        for rect in self.obstacles:
            pygame.draw.rect(self.ecran, ROUGE, rect)

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
        while True:
            if any(event.type in [pygame.QUIT, pygame.KEYDOWN] for event in pygame.event.get()):
                pygame.quit()
                return

