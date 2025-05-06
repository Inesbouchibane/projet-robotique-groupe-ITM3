from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import (
    Geom, GeomNode, GeomTriangles, GeomVertexData, GeomVertexFormat,
    GeomVertexWriter,
    NodePath, LineSegs, VBase4, Point3, Texture, OmniBoundingVolume,
    WindowProperties, FrameBufferProperties, GraphicsOutput,
    DirectionalLight, AmbientLight, GeomLines,
    GraphicsPipe
)
from panda3d.core import LVector3, LPoint3

import numpy as np
import cv2
from math import cos, sin, radians, degrees, sqrt
from src.utils import getDistanceFromPts
from logging import getLogger
import sys
import time
import os

logger = getLogger(__name__)

# Couleurs (RGBA)
FOND = (0.8, 0.9, 1.0, 1.0)
SOL = (0.6, 0.8, 0.6, 1.0)
ROBOT = (0.2, 0.8, 0.2, 1.0)
ROBOT_CRASH = (1.0, 0.6, 0.2, 1.0)
OBSTACLE = (0.3, 0.3, 0.3, 1.0)
TRAJET = (1.0, 1.0, 1.0, 1.0)
DIRECTION = (0.9, 0.9, 0.2, 1.0)
BALISE_BLEU = (0.0, 0.0, 1.0, 1.0)
BALISE_ROUGE = (1.0, 0.0, 0.0, 1.0)
BALISE_VERT = (0.0, 0.5, 0.0, 1.0)
BALISE_JAUNE = (1.0, 1.0, 0.0, 1.0)


class Affichage3D(ShowBase):
    def __init__(self, largeur, hauteur, obstacles_points):
        ShowBase.__init__(self)

        # Configuration de la fenêtre
        props = WindowProperties()
        props.setTitle("ITM3-Simulation3D")
        props.setSize(largeur, hauteur)
        self.win.requestProperties(props)

        # Désactiver les contrôles de caméra par défaut
        self.disableMouse()

        # Limiter le frame rate à 60 FPS
        self.setFrameRateMeter(True)
        globalClock.setMode(globalClock.MLimited)
        globalClock.setFrameRate(60.0)

        # Configuration du fond
        self.setBackgroundColor(*FOND)

        # Paramètres de l'environnement
        self.envi = None
        self.largeur, self.hauteur = largeur, hauteur
        self.obstacles_points = obstacles_points
        self.trajet = []
        self.last_position = None
        self.hauteur_obstacle = 50

        # Paramètres de la caméra
        self.cam_mode = 0
        self.cam_x = 500
        self.cam_y = 250
        self.cam_z = 600
        self.angle_h = 0
        self.angle_v = 45
        self.lateral_view = None

        # Balise (réduite en taille)
        self.beacon_position = [600, 300]
        self.beacon_size = 40  # Réduit
        self.balise = None  # Balise non initialisée au départ
        self.showBalise = False  # Balise cachée au départ
        self.fixed_beacon = False  # Flag to control beacon movement

        # Initialisation des noeuds
        self.scene = self.render.attachNewNode("Scene")
        self.dessiner_sol()
        self.dessiner_obstacles()

        # Éclairage
        self.setup_lighting()

        # Trajet
        self.trajet_node = None

        # Robot
        self.robot_node = None

        # Balise
        self.balise_node = None

        # Tâche principale
        self.taskMgr.add(self.update_task, "UpdateTask")

        # Contrôleur et adaptateur
        self.controleur = None
        self.adaptateur = None
        self.robot = None

        # Buffer pour capture d'image
        self.buffer = None
        self.buffer_texture = None
        self.setup_buffer()

        logger.debug("Affichage3D initialisé")

    def setup_lighting(self):
        """Configure l'éclairage de la scène."""
        ambient_light = AmbientLight("ambient_light")
        ambient_light.setColor((0.3, 0.3, 0.3, 1))
        ambient_np = self.render.attachNewNode(ambient_light)
        self.render.setLight(ambient_np)

        directional_light = DirectionalLight("directional_light")
        directional_light.setColor((0.7, 0.7, 0.7, 1))
        directional_light.setDirection(LVector3(0, -1, -1))
        directional_np = self.render.attachNewNode(directional_light)
        self.render.setLight(directional_np)

        logger.debug("Éclairage configuré")

    def set_controleur(self, controleur):
        """Définit le contrôleur pour les stratégies."""
        self.controleur = controleur
        logger.debug("Contrôleur défini")

    def set_adaptateur(self, adaptateur):
        """Définit l'adaptateur et transmet l'image capturée."""
        self.adaptateur = adaptateur
        logger.debug("Adaptateur défini")

    def setup_buffer(self):
        """Configure un buffer hors écran pour capturer les images."""
        fb_props = FrameBufferProperties()
        fb_props.setRgbaBits(8, 8, 8, 8)  # RGBA buffer
        fb_props.setDepthBits(16)  # Depth buffer for 3D rendering
        fb_props.setStencilBits(8)  # Optional stencil buffer
        win_props = WindowProperties.size(self.largeur, self.hauteur)  # Match window size

        try:
            # Ensure graphics pipe is initialized
            if not hasattr(self, 'pipe') or self.pipe is None:
                self.pipe = self.graphicsEngine.getDefaultPipe()
                logger.debug(f"Graphics pipe initialized: {self.pipe}")

            logger.debug("Initialisation du pipeline graphique pour le buffer")
            # Create offscreen buffer
            self.buffer = self.graphicsEngine.makeOutput(
                self.pipe,
                "offscreen_buffer",
                -100,  # Lower priority than main window
                fb_props,
                win_props,
                GraphicsOutput.RTMCopyRam,  # Copy to RAM for screenshot
                self.win.getGsg(),
                self.win
            )
            if not self.buffer:
                logger.error("Échec de la création du buffer : vérifiez les pilotes OpenGL, la mémoire GPU ou la compatibilité")
                self.buffer = None
                self.buffer_texture = None
                return

            logger.debug(f"Buffer créé avec succès: {self.buffer}")
            self.buffer.setClearColor(FOND)  # Set clear color
            self.buffer.setSort(-100)  # Render before main window
            self.buffer.setActive(True)

            # Create texture for buffer
            self.buffer_texture = Texture()
            self.buffer.addRenderTexture(self.buffer_texture, GraphicsOutput.RTMCopyRam)
            logger.debug(f"Texture créée: {self.buffer_texture}")

            # Create camera for buffer
            buffer_camera = self.makeCamera(self.buffer)
            buffer_camera.node().setScene(self.render)
            buffer_camera.node().setLens(self.cam.node().getLens())  # Match main camera lens

            logger.debug("Buffer hors écran configuré avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la configuration du buffer : {e}")
            self.buffer = None
            self.buffer_texture = None
            # Fallback: Log system info for debugging
            logger.debug(f"Panda3D version: {sys.modules['panda3d'].__version__}")
            logger.debug(f"Graphics pipe type: {self.pipe.getType() if self.pipe else 'None'}")

    def changer_mode_camera(self, delta):
        """Change le mode de la caméra (zoom avant/arrière)."""
        self.lateral_view = None
        self.cam_mode = max(0, min(2, self.cam_mode + delta))
        if self.cam_mode == 0:
            self.cam_z = 600
        logger.debug(f"Mode caméra : {self.cam_mode}")

    def changer_lateral_view(self, side):
        """Active la vue latérale gauche ou droite."""
        self.lateral_view = side
        self.cam_mode = 0
        logger.debug(f"Vue latérale {side} activée")

    def update_task(self, task):
        """Tâche principale pour mettre à jour la scène."""
        if not hasattr(self, 'robot') or self.robot is None:
            return Task.cont
        if self.adaptateur:
            if hasattr(self.adaptateur, 'step'):
                self.adaptateur.step()  # Mettre à jour la position du robot
            if self.envi:
                self.envi.refreshEnvironnement()  # Vérifier les collisions
        self.mettre_a_jour(self.robot)
        self.updateImg()
        return Task.cont

    def update_environnement(self, environnement):
        """Met à jour la position de la balise dans l'environnement."""
        self.envi = environnement
        if self.envi and self.showBalise and self.balise:
            self.envi.beacon_position = tuple(self.beacon_position)
        logger.debug(f"Environnement mis à jour avec balise à {self.beacon_position}")

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
                cam_x = self.cam_x + math.cos(math.radians(self.angle_h)) * self.cam_z * \
                    math.cos(math.radians(self.angle_v))
                cam_y = self.cam_y + math.sin(math.radians(self.angle_h)) * self.cam_z * \
                    math.cos(math.radians(self.angle_v))
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
        """Dessine le sol avec une grille."""
        vdata = GeomVertexData("sol", GeomVertexFormat.getV3c4(), Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, "vertex")
        color = GeomVertexWriter(vdata, "color")

        vertex.addData3(0, 0, 0)
        vertex.addData3(self.largeur, 0, 0)
        vertex.addData3(self.largeur, self.hauteur, 0)
        vertex.addData3(0, self.hauteur, 0)
        for _ in range(4):
            color.addData4(*SOL)

        for x in range(0, int(self.largeur), 100):
            for y in range(0, int(self.hauteur), 100):
                vertex.addData3(x, y, 0.1)
                vertex.addData3(x + 50, y, 0.1)
                vertex.addData3(x + 50, y + 50, 0.1)
                vertex.addData3(x, y + 50, 0.1)
                for _ in range(4):
                    color.addData4(1.0, 1.0, 1.0, 1.0)

        geom = Geom(vdata)
        tris = GeomTriangles(Geom.UHStatic)
        base_idx = 0
        tris.addVertices(0, 1, 2)
        tris.addVertices(0, 2, 3)
        base_idx += 4
        for _ in range(0, int(self.largeur * self.hauteur / 10000)):
            tris.addVertices(base_idx, base_idx + 1, base_idx + 2)
            tris.addVertices(base_idx, base_idx + 2, base_idx + 3)
            base_idx += 4
        geom.addPrimitive(tris)

        node = GeomNode("sol")
        node.addGeom(geom)
        self.scene.attachNewNode(node)
        logger.debug("Sol avec grille dessiné")

    def dessiner_obstacles(self):
        """Dessine tous les obstacles comme des prismes."""
        for points in self.obstacles_points:
            if len(points) < 3:
                continue
            vdata = GeomVertexData("obstacle", GeomVertexFormat.getV3c4(),
                                   Geom.UHStatic)
            vertex = GeomVertexWriter(vdata, "vertex")
            color = GeomVertexWriter(vdata, "color")

            for x, y in points:
                vertex.addData3(x, y, 0)
                color.addData4(*OBSTACLE)
            for x, y in points:
                vertex.addData3(x, y, self.hauteur_obstacle)
                color.addData4(*OBSTACLE)
            for x, y in points:
                vertex.addData3(x, y, self.hauteur_obstacle)
                color.addData4(0.5, 0.5, 0.5, 1.0)

            geom = Geom(vdata)
            tris = GeomTriangles(Geom.UHStatic)
            n = len(points)
            for i in range(n):
                i1, i2 = i, (i + 1) % n
                tris.addVertices(i1, i2, i2 + n)
                tris.addVertices(i1, i2 + n, i1 + n)
            base_idx = 2 * n
            for i in range(1, n - 1):
                tris.addVertices(base_idx, base_idx + i, base_idx + i + 1)

            geom.addPrimitive(tris)
            node = GeomNode("obstacle")
            node.addGeom(geom)
            self.scene.attachNewNode(node)
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
