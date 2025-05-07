import pygame
from src import (
    StrategieAvancer, StrategieAuto, setStrategieCarre, StrategieArretMur, StrategieSuivreBalise
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

def lancer_strategie(affichage3d, strategie_type):
    """Lance une stratégie via le contrôleur ou gère la visibilité de la balise."""
    if affichage3d.controleur is None and strategie_type != "suivre_balise":
        logger.error("Contrôleur non défini")
        return
    try:
        if strategie_type == "tracer_carre":
            affichage3d.controleur.set_strategie("tracer_carre", longueur_cote=100)
            affichage3d.fixed_beacon = False
        elif strategie_type == "avancer":
            affichage3d.controleur.set_strategie("avancer", distance=100)
            affichage3d.fixed_beacon = False
        elif strategie_type == "auto":
            affichage3d.controleur.set_strategie("auto", vitAngG=14, vitAngD=7)
            affichage3d.fixed_beacon = False
        elif strategie_type == "arret_mur":
            affichage3d.controleur.set_strategie("arret_mur", adaptateur=affichage3d.adaptateur, distance_arret=5)
            affichage3d.fixed_beacon = False
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
        affichage3d.controleur.lancerStrategie()
        logger.info(f"Stratégie '{strategie_type}' lancée")
    except Exception as e:
        logger.error(f"Erreur lors du lancement de la stratégie {strategie_type} : {e}")