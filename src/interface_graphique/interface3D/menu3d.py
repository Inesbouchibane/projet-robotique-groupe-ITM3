# src/interface_graphique/interface3D/menu3d.py

import pygame
from src import (
    StrategieAvancer, StrategieAuto, setStrategieCarre
)
from logging import getLogger

logger = getLogger(__name__)
    elif strategie_type == "suivre_balise":
            if not affichage3d.showBalise:
                # Afficher la balise
                affichage3d.showBalise = True
                if not affichage3d.balise and affichage3d.robot:
                    # Positionner la balise devant le robot
                    cos_a, sin_a = affichage3d.robot.direction[0], affichage3d.robot.direction[1]
                    distance_from_robot = 100
                    beacon_x = affichage3d.robot.x + cos_a * distance_from_robot
                    beacon_y = affichage3d.robot.y + sin_a * distance_from_robot
                    beacon_x = max(0, min(affichage3d.largeur, beacon_x))
                    beacon_y = max(0, min(affichage3d.hauteur, beacon_y))
                    affichage3d.beacon_position = [beacon_x, beacon_y]
                    from interface3d import Balise  # Importer ici pour éviter dépendance circulaire
                    affichage3d.balise = Balise(beacon_x, beacon_y, 40, 30)
                affichage3d.fixed_beacon = True
                logger.info("Balise affichée")
                affichage3d.controleur.set_strategie("suivre_balise", adaptateur=affichage3d.adaptateur)
                affichage3d.controleur.lancerStrategie()
            else:
                # Cacher la balise
                affichage3d.showBalise = False
                affichage3d.fixed_beacon = False
                if affichage3d.balise_node:
                    affichage3d.balise_node.removeNode()
                    affichage3d.balise_node = None
                if affichage3d.balise:
                    affichage3d.balise = None
                logger.info("Balise cachée")
                return  # Ne pas lancer de stratégie si on cache

def afficher_instructions():
    print("Commandes disponibles dans la fenêtre 3D :")
    print("- 'c' : Tracer un carré (100 unités)")
    print("- 'a' : Avancer (100 unités)")
    print("- 'r' : Mode automatique (vitesses 14, 7)")
    print("- 'ESC' : Quitter")
    print("- 'UP' : Zoom avant (haut → rapprochée → vue du robot)")
    print("- 'DOWN' : Zoom arrière (robot → rapprochée → haut)")
    print("- 'LEFT' : Vue à gauche du robot")
    print("- 'RIGHT' : Vue à droite du robot")
