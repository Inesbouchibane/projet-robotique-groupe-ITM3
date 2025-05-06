import pygame
from src import (
    StrategieAvancer, StrategieAuto, setStrategieCarre, StrategieArretMur, 
StrategieSuivreBalise
)
from logging import getLogger

logger = getLogger(__name__)

def afficher_instructions():
    print("Commandes disponibles dans la fenêtre 3D :")
    print("- 'c' : Tracer un carré (100 unités)")
    print("- 'a' : Avancer (100 unités)")
    print("- 'r' : Mode automatique (vitesses 14, 7)")
    print("- 'm' : S'approcher à 5 mm d'un mur/obstacle")
    print("- 'b' : Suivre la balise")
    print("- 'ESC' : Quitter")
    print("- 'UP' : Zoom avant (haut → rapprochée → vue du robot)")
    print("- 'DOWN' : Zoom arrière (robot → rapprochée → haut)")
    print("- 'LEFT' : Vue à gauche du robot")
    print("- 'RIGHT' : Vue à droite du robot")

def gerer_touches(affichage3d):
    """Configure la gestion des touches pour l'interface 3D."""
    # Associer les touches aux actions
    affichage3d.accept("escape", affichage3d.quitter)
    affichage3d.accept("c", lancer_strategie, [affichage3d, "tracer_carre"])
    affichage3d.accept("a", lancer_strategie, [affichage3d, "avancer"])
    affichage3d.accept("r", lancer_strategie, [affichage3d, "auto"])
    affichage3d.accept("m", lancer_strategie, [affichage3d, "arret_mur"])
    affichage3d.accept("b", lancer_strategie, [affichage3d, "suivre_balise"])
    affichage3d.accept("arrow_up", affichage3d.changer_mode_camera, [1])
    affichage3d.accept("arrow_down", affichage3d.changer_mode_camera, [-1])
    affichage3d.accept("arrow_left", affichage3d.changer_lateral_view, ["left"])
    affichage3d.accept("arrow_right", affichage3d.changer_lateral_view, ["right"])
    affichage3d.accept("mouse1", affichage3d.createBalise, [None])
    logger.debug("Gestion des touches configurée dans menu3d")
