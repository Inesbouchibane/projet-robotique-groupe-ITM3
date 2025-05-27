from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import (
    Geom, GeomNode, GeomTriangles, GeomVertexData, GeomVertexFormat, GeomVertexWriter,
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
        
        # Initialize last update time
        self.last_update_time = time.time()
        
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
        
        # Calculate delta_t
        current_time = time.time()
        delta_t = current_time - self.last_update_time
        self.last_update_time = current_time
        
        if self.adaptateur:
            if hasattr(self.adaptateur, 'step'):
                self.adaptateur.step(delta_t)  # Mettre à jour la position du robot
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
        """Met à jour le rendu de la scène."""
        self.robot = robot
        cos_a, sin_a = robot.direction[0], robot.direction[1]
        
        if not self.fixed_beacon and self.showBalise and self.balise:
            self.update_beacon_position(robot)  # Mettre à jour si balise visible et non fixée
        self.gerer_camera(robot)
        
        current_position = (robot.x, robot.y)
        if self.last_position is None or getDistanceFromPts(current_position, self.last_position) > 1:
            self.trajet.append(current_position)
            self.last_position = current_position
            self.update_trajet()
        
        if self.robot_node:
            self.robot_node.removeNode()
        self.robot_node = self.dessiner_robot(robot)
        
        if self.balise_node:
            self.balise_node.removeNode()
            self.balise_node = None
        if self.showBalise and self.balise:
            self.balise_node = self.dessiner_balise(robot)
        
        logger.debug(f"Scène mise à jour : robot à ({robot.x:.2f}, {robot.y:.2f})")

    def update_beacon_position(self, robot):
        """Repositionne la balise devant le robot, si non fixée."""
        cos_a, sin_a = self.robot.direction[0], self.robot.direction[1]
        distance_from_robot = 100
        self.beacon_position[0] = robot.x + cos_a * distance_from_robot
        self.beacon_position[1] = robot.y + sin_a * distance_from_robot
        self.beacon_position[0] = max(0, min(self.largeur, self.beacon_position[0]))
        self.beacon_position[1] = max(0, min(self.hauteur, self.beacon_position[1]))
        self.balise.x, self.balise.y = self.beacon_position[0], self.beacon_position[1]
        logger.debug(f"Balise repositionnée à ({self.beacon_position[0]:.2f}, {self.beacon_position[1]:.2f})")

    def gerer_camera(self, robot):
        """Configure la caméra selon le mode."""
        cos_a, sin_a = robot.direction[0], robot.direction[1]
        cam_x, cam_y, cam_z = 0, 0, 0
        look_x, look_y, look_z = 0, 0, 0

        if self.lateral_view == "left":
            cam_x = robot.x - sin_a * 100
            cam_y = robot.y + cos_a * 100
            cam_z = 100
            look_x, look_y, look_z = robot.x, robot.y, 0
        elif self.lateral_view == "right":
            cam_x = robot.x + sin_a * 100
            cam_y = robot.y - cos_a * 100
            cam_z = 100
            look_x, look_y, look_z = robot.x, robot.y, 0
        else:
            if self.cam_mode == 0:
                cam_x = self.cam_x + cos(radians(self.angle_h)) * self.cam_z * cos(radians(self.angle_v))
                cam_y = self.cam_y + sin(radians(self.angle_h)) * self.cam_z * cos(radians(self.angle_v))
                cam_z = self.cam_z * sin(radians(self.angle_v))
                look_x, look_y, look_z = 500, 250, 0
            elif self.cam_mode == 1:
                cam_x = robot.x - cos_a * 100
                cam_y = robot.y - sin_a * 100
                cam_z = 200
                look_x, look_y, look_z = robot.x, robot.y, 0
            elif self.cam_mode == 2:
                cam_x = robot.x + cos_a * 30
                cam_y = robot.y + sin_a * 30
                cam_z = 10
                look_x = robot.x + cos_a * 150
                look_y = robot.y + sin_a * 150
                look_z = 10

        self.camera.setPos(cam_x, cam_y, cam_z)
        self.camera.lookAt(look_x, look_y, look_z)
        logger.debug(f"Caméra positionnée : mode={self.cam_mode}, pos=({cam_x:.2f}, {cam_y:.2f}, {cam_z:.2f})")

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
            vdata = GeomVertexData("obstacle", GeomVertexFormat.getV3c4(), Geom.UHStatic)
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
        """Dessine le robot comme un parallélépipède avec une ligne de direction."""
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
        
        vdata = GeomVertexData("robot", GeomVertexFormat.getV3c4(), Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, "vertex")
        color = GeomVertexWriter(vdata, "color")
        
        for x, y in points_base:
            vertex.addData3(x, y, 0)
            color.addData4(*couleur)
        for x, y in points_base:
            vertex.addData3(x, y, hauteur_robot)
            color.addData4(*couleur)
        for x, y in points_base:
            vertex.addData3(x, y, hauteur_robot)
            color.addData4(couleur[0] * 0.8, couleur[1] * 0.8, couleur[2] * 0.8, 1)
        
        vertex.addData3(robot.x, robot.y, hauteur_robot + 5)
        vertex.addData3(robot.x + cos_a * 30, robot.y + sin_a * 30, hauteur_robot + 5)
        color.addData4(*DIRECTION)
        color.addData4(*DIRECTION)
        
        geom_tris = Geom(vdata)
        tris = GeomTriangles(Geom.UHStatic)
        for i in range(4):
            i1, i2 = i, (i + 1) % 4
            tris.addVertices(i1, i2, i2 + 4)
            tris.addVertices(i1, i2 + 4, i1 + 4)
        for i in range(1, 3):
            tris.addVertices(8, 8 + i, 8 + i + 1)
        geom_tris.addPrimitive(tris)
        
        geom_lines = Geom(vdata)
        lines = GeomLines(Geom.UHStatic)
        lines.addVertices(12, 13)
        geom_lines.addPrimitive(lines)
        
        node_tris = GeomNode("robot_tris")
        node_tris.addGeom(geom_tris)
        node_lines = GeomNode("robot_lines")
        node_lines.addGeom(geom_lines)
        
        robot_np = self.scene.attachNewNode("robot")
        robot_np.attachNewNode(node_tris)
        robot_np.attachNewNode(node_lines)
        
        return robot_np

    def dessiner_balise(self, robot):
        """Dessine la balise à sa position actuelle si elle est visible."""
        if not self.showBalise or not self.balise:
            return None
        if self.balise_node:
            self.balise_node.removeNode()
        self.balise_node = self.createBalise(self.balise)
        return self.balise_node

    def createBalise(self, balise):
        """Crée une balise (objet) aux coordonnées de la souris.
        :param balise: la balise que l'on souhaite créer
        :returns: le NodePath vers la balise créée (objet3D)
        """
        if balise is None:
            self.showBalise = True  # Afficher la balise lors d'un clic
            if not self.balise and self.robot:
                # Positionner devant le robot par défaut
                cos_a, sin_a = self.robot.direction[0], self.robot.direction[1]
                distance_from_robot = 100
                beacon_x = self.robot.x + cos_a * distance_from_robot
                beacon_y = self.robot.y + sin_a * distance_from_robot
                beacon_x = max(0, min(self.largeur, beacon_x))
                beacon_y = max(0, min(self.hauteur, beacon_y))
                self.beacon_position = [beacon_x, beacon_y]
                self.balise = Balise(beacon_x, beacon_y, 40, 30)
        else:
            self.balise = balise

        # Récupérer le robot sélectionné
        if hasattr(self, 'envi') and self.envi and hasattr(self.envi, 'listeRobots') and self.envi.listeRobots:
            robot = self.envi.listeRobots[self.envi.robotSelect].robot if hasattr(self.envi, 'robotSelect') else self.robot
        else:
            robot = self.robot
            logger.warning("Environnement ou robot non défini")

        # Direction orthogonale à celle du robot
        self.balise.dir[1] = robot.direction[0]
        self.balise.dir[0] = robot.direction[1]

        if self.mouseWatcherNode.hasMouse():  # Si la souris est sur l'écran
            mouse_x = self.mouseWatcherNode.getMouseX()
            mouse_y = self.mouseWatcherNode.getMouseY()
            self.balise.x = (mouse_x + 1) * self.largeur / 2  # Map [-1,1] to [0,largeur]
            self.balise.y = (1 - mouse_y) * self.hauteur / 2   # Map [-1,1] to [0,hauteur]
            self.beacon_position = [self.balise.x, self.balise.y]
            self.fixed_beacon = True  # Fixer la position après clic
            logger.debug(f"Balise placée via souris à ({self.balise.x:.2f}, {self.balise.y:.2f})")
        else:
            logger.warning("Pas de souris à l'écran, placement par défaut")
            self.balise.x = self.beacon_position[0]  # Utiliser la position actuelle
            self.balise.y = self.beacon_position[1]
            logger.debug(f"Balise placée par défaut à ({self.balise.x:.2f}, {self.balise.y:.2f})")

        # Définir le format des sommets avec coordonnées de texture
        self.balise.format = GeomVertexFormat.getV3t2()
        self.balise.vdata = GeomVertexData("balise", self.balise.format, Geom.UHDynamic)

        # Créer des writers pour les sommets et les coordonnées de texture
        self.balise.vertexBal = GeomVertexWriter(self.balise.vdata, "vertex")
        self.balise.texcoord = GeomVertexWriter(self.balise.vdata, "texcoord")

        # Ajouter les sommets et les coordonnées de texture
        half_width = self.balise.width / 2
        self.balise.vertexBal.addData3f(self.balise.x - half_width * self.balise.dir[0], self.balise.y - half_width * self.balise.dir[1], 0)
        self.balise.texcoord.addData2f(1, 0)

        self.balise.vertexBal.addData3f(self.balise.x + half_width * self.balise.dir[0], self.balise.y + half_width * self.balise.dir[1], 0)
        self.balise.texcoord.addData2f(0, 0)

        self.balise.vertexBal.addData3f(self.balise.x - half_width * self.balise.dir[0], self.balise.y - half_width * self.balise.dir[1], self.balise.height)
        self.balise.texcoord.addData2f(1, 1)

        self.balise.vertexBal.addData3f(self.balise.x + half_width * self.balise.dir[0], self.balise.y + half_width * self.balise.dir[1], self.balise.height)
        self.balise.texcoord.addData2f(0, 1)

        self.balise.balise = GeomTriangles(Geom.UHDynamic)
        self.balise.balise.addVertices(0, 1, 2)
        self.balise.balise.addVertices(1, 2, 3)

        self.balise.geom = Geom(self.balise.vdata)
        self.balise.geom.addPrimitive(self.balise.balise)

        node = GeomNode("balise")
        node.addGeom(self.balise.geom)

        self.balise.np = self.render.attachNewNode(node)
        self.balise.np.setTwoSided(True)  # Pour rendre toutes les faces visibles
        self.balise.np.node().setBounds(OmniBoundingVolume())
        self.balise.np.node().setFinal(True)

        # Charger la texture depuis le dossier assets
        image_path = os.path.join(os.path.dirname(__file__), "assets", "beacon_image.png")
        logger.debug(f"Tentative de chargement de l'image à : {image_path}")
        texture = Texture()
        if not texture.read(image_path):
            logger.error(f"Échec du chargement de l'image : {image_path}. Vérifiez le fichier.")
            self.balise.np.setColor(1.0, 0.0, 0.0, 1.0)  # Fallback: rouge
        else:
            logger.debug(f"Texture chargée avec succès depuis : {image_path}")
            self.balise.np.setTexture(texture)
            self.balise.np.setTransparency(True)

        return self.balise.np

    def update_trajet(self):
        """Met à jour le trajet du robot."""
        if self.trajet_node:
            self.trajet_node.removeNode()
        if len(self.trajet) > 1:
            segs = LineSegs()
            segs.setColor(*TRAJET)
            segs.setThickness(2)
            for x, y in self.trajet:
                segs.drawTo(x, y, 1)
            self.trajet_node = self.scene.attachNewNode(segs.create())
            logger.debug(f"Trajet mis à jour avec {len(self.trajet)} points")

    def getImageInterface(self):
        """Capture le framebuffer et retourne une image BGR."""
        if not self.buffer or not self.buffer_texture:
            logger.error("Buffer ou texture non configuré, retour d'une image vide")
            return np.zeros((self.hauteur, self.largeur, 3), dtype=np.uint8)  # Fallback: blank image
        
        try:
            self.graphicsEngine.renderFrame()
            image = self.buffer.getScreenshot()
            if not image:
                logger.error("Échec de la capture de l'image via screenshot")
                return np.zeros((self.hauteur, self.largeur, 3), dtype=np.uint8)
                
            # Convertir l'image Panda3D en tableau NumPy
            image_data = image.getRamImageAs("RGBA")
            if not image_data:
                logger.error("Échec de l'extraction des données de l'image")
                return np.zeros((self.hauteur, self.largeur, 3), dtype=np.uint8)
                
            image_array = np.frombuffer(image_data, dtype=np.uint8)
            image_array = image_array.reshape((image.getYSize(), image.getXSize(), 4))
            image_array = image_array[::-1]  # Inverser verticalement
            image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)
            
            logger.debug(f"Image capturée : taille={image_bgr.shape}")
            return image_bgr
        except Exception as e:
            logger.error(f"Erreur lors de la capture d'image : {e}")
            return np.zeros((self.hauteur, self.largeur, 3), dtype=np.uint8)

    def updateImg(self):
        """Met à jour l'image du robot avec la capture de la caméra simulée."""
        if hasattr(self, 'robot') and self.robot:
            self.robot.img = self.getImageInterface()
            logger.debug("Image du robot mise à jour")

    def quitter(self):
        """Quitte l'application."""
        self.running = False
        self.userExit()
        logger.info("Application terminée")

class Balise:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dir = [0, 0]
        self.format = None
        self.vdata = None
        self.vertexBal = None
        self.texcoord = None
        self.balise = None
        self.geom = None
        self.np = None