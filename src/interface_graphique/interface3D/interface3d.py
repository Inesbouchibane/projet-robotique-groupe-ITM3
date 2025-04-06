# src/interface_graphique/interface3D/interface3d.py

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from src.utils import getDistanceFromPts
from logging import getLogger
import math

logger = getLogger(__name__)

# Couleurs simples et claires (R, G, B, A)
FOND = (0.8, 0.9, 1.0, 1.0)      # Bleu ciel pâle
SOL = (0.6, 0.8, 0.6, 1.0)       # Vert pâle
ROBOT = (0.2, 0.8, 0.2, 1.0)     # Vert clair
ROBOT_CRASH = (1.0, 0.6, 0.2, 1.0)  # Orange doux pour collision
OBSTACLE = (0.3, 0.3, 0.3, 1.0)  # Gris foncé
TRAJET = (1.0, 1.0, 1.0, 1.0)    # Blanc
DIRECTION = (0.9, 0.9, 0.2, 1.0) # Jaune pâle

class Affichage3D:
    def __init__(self, largeur, hauteur, obstacles_points):
        pygame.init()
        self.largeur, self.hauteur = largeur, hauteur
        pygame.display.set_mode((largeur, hauteur), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("ITM3-Simulation3D")
        
        glClearColor(*FOND)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(60, (largeur / hauteur), 0.1, 2000.0)
        glMatrixMode(GL_MODELVIEW)
        glDisable(GL_LIGHTING)
        
        self.obstacles_points = obstacles_points
        self.trajet = []
        self.last_position = None
        self.hauteur_obstacle = 50
        
        self.cam_mode = 0  # 0: haut, 1: rapprochée, 2: robot
        self.cam_x = 500
        self.cam_y = 250
        self.cam_z = 600
        self.angle_h = 0
        self.angle_v = 45
        self.lateral_view = None

    def mettre_a_jour(self, robot):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.gerer_camera(robot)
        
        glLoadIdentity()
        cos_a, sin_a = robot.direction[0], robot.direction[1]
        if self.lateral_view == "left":
            gluLookAt(
                robot.x - sin_a * 100,
                robot.y + cos_a * 100,
                100,
                robot.x, robot.y, 0,
                0, 0, 1
            )
        elif self.lateral_view == "right":
            gluLookAt(
                robot.x + sin_a * 100,
                robot.y - cos_a * 100,
                100,
                robot.x, robot.y, 0,
                0, 0, 1
            )
        else:
            if self.cam_mode == 0:  # Vue de haut
                cam_x = self.cam_x + math.cos(math.radians(self.angle_h)) * self.cam_z * math.cos(math.radians(self.angle_v))
                cam_y = self.cam_y + math.sin(math.radians(self.angle_h)) * self.cam_z * math.cos(math.radians(self.angle_v))
                cam_z = self.cam_z * math.sin(math.radians(self.angle_v))
                look_x, look_y, look_z = 500, 250, 0
            elif self.cam_mode == 1:  # Vue rapprochée
                cam_x = robot.x - cos_a * 100
                cam_y = robot.y - sin_a * 100
                cam_z = 200
                look_x, look_y, look_z = robot.x, robot.y, 0
            elif self.cam_mode == 2:  # Vue "du robot"
                cam_x = robot.x + cos_a * 30
                cam_y = robot.y + sin_a * 30
                cam_z = 10
                look_x = robot.x + cos_a * 150
                look_y = robot.y + sin_a * 150
                look_z = 10
            
            gluLookAt(
                cam_x, cam_y, cam_z,
                look_x, look_y, look_z,
                0, 0, 1
            )
        
        self.dessiner_sol()
        for points in self.obstacles_points:
            self.dessiner_obstacle(points)
        
        current_position = (robot.x, robot.y)
        if self.last_position is None or getDistanceFromPts(current_position, self.last_position) > 1:
            self.trajet.append(current_position)
            self.last_position = current_position
        
        if len(self.trajet) > 1:
            glBegin(GL_LINE_STRIP)
            glColor4f(*TRAJET)
            for x, y in self.trajet:
                glVertex3f(x, y, 1)
            glEnd()
        
        self.dessiner_robot(robot)
        
        pygame.display.flip()
        pygame.time.wait(10)

    def gerer_camera(self, robot):
        for event in pygame.event.poll(), pygame.event.peek():
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                logger.info(f"Touche caméra pressée : {key_name}")
                if event.key == pygame.K_UP:
                    self.lateral_view = None
                    self.cam_mode = min(self.cam_mode + 1, 2)
                    logger.debug(f"Mode caméra : {self.cam_mode}")
                elif event.key == pygame.K_DOWN:
                    self.lateral_view = None
                    self.cam_mode = max(self.cam_mode - 1, 0)
                    self.cam_z = 600
                    logger.debug(f"Mode caméra : {self.cam_mode}")
                elif event.key == pygame.K_LEFT:
                    self.lateral_view = "left"
                    self.cam_mode = 0
                    logger.debug("Vue latérale gauche activée")
                elif event.key == pygame.K_RIGHT:
                    self.lateral_view = "right"
                    self.cam_mode = 0
                    logger.debug("Vue latérale droite activée")

    def dessiner_sol(self):
        glBegin(GL_QUADS)
        glColor4f(*SOL)
        glVertex3f(0, 0, 0)
        glVertex3f(self.largeur, 0, 0)
        glVertex3f(self.largeur, self.hauteur, 0)
        glVertex3f(0, self.hauteur, 0)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        for x in range(0, int(self.largeur), 100):
            for y in range(0, int(self.hauteur), 100):
                glVertex3f(x, y, 0.1)
                glVertex3f(x + 50, y, 0.1)
                glVertex3f(x + 50, y + 50, 0.1)
                glVertex3f(x, y + 50, 0.1)
        glEnd()
        logger.debug("Sol avec carrés dessiné")

    def dessiner_obstacle(self, points):
        if len(points) < 3:
            return
        glBegin(GL_QUAD_STRIP)
        glColor4f(*OBSTACLE)
        for i in range(len(points) + 1):
            idx = i % len(points)
            x, y = points[idx]
            glVertex3f(x, y, 0)
            glVertex3f(x, y, self.hauteur_obstacle)
        glEnd()
        glBegin(GL_POLYGON)
        glColor4f(0.5, 0.5, 0.5, 1)
        for x, y in points:
            glVertex3f(x, y, self.hauteur_obstacle)
        glEnd()
        glBegin(GL_LINE_LOOP)
        glColor4f(0.0, 0.0, 0.0, 1.0)
        for x, y in points:
            glVertex3f(x, y, self.hauteur_obstacle + 0.1)
        glEnd()
        logger.debug(f"Obstacle dessiné avec points : {points}")

    def dessiner_robot(self, robot):
        cos_a, sin_a = robot.direction[0], robot.direction[1]
        points_base = [
            (robot.x + cos_a * robot.length / 2 - sin_a * robot.width / 2,
             robot.y + sin_a * robot.length / 2 + cos_a * robot.width / 2),
            (robot.x - cos_a * robot.length / 2 - sin_a * robot.width / 2,
             robot.y - sin_a * robot.length / 2 + cos_a * robot.width / 2),
            (robot.x - cos_a * robot.length / 2 + sin_a * robot.width / 2,
             robot.y - sin_a * robot.length / 2 - cos_a * robot.width / 2),
            (robot.x + cos_a * robot.length / 2 + sin_a * robot.width / 2,
             robot.y + sin_a * robot.length / 2 - cos_a * robot.width / 2)
        ]
        
        hauteur_robot = 30
        couleur = ROBOT_CRASH if robot.estCrash else ROBOT
        
        glBegin(GL_QUADS)
        glColor4f(*couleur)
        for x, y in points_base:
            glVertex3f(x, y, 0)
        glEnd()
        
        glBegin(GL_QUAD_STRIP)
        glColor4f(*couleur)
        for i in range(len(points_base) + 1):
            idx = i % len(points_base)
            x, y = points_base[idx]
            glVertex3f(x, y, 0)
            glVertex3f(x, y, hauteur_robot)
        glEnd()
        
        glBegin(GL_POLYGON)
        glColor4f(couleur[0] * 0.8, couleur[1] * 0.8, couleur[2] * 0.8, 1)
        for x, y in points_base:
            glVertex3f(x, y, hauteur_robot)
        glEnd()
        
        glBegin(GL_LINES)
        glColor4f(*DIRECTION)
        glVertex3f(robot.x, robot.y, hauteur_robot + 5)
        glVertex3f(robot.x + cos_a * 30, robot.y + sin_a * 30, hauteur_robot + 5)
        glEnd()
        logger.debug(f"Robot dessiné à ({robot.x}, {robot.y})")

    def attendre_fermeture(self):
        pygame.quit()