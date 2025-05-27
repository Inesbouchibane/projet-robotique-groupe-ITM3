import pygame
from src.controleur.strategies import StrategieAvancer, StrategieAuto, setStrategieCarre, StrategieArretMur, StrategieSuivreBalise, StrategieClavier, StrategieTourner  # Add StrategieTourner
from logging import getLogger
from direct.task import Task

logger = getLogger(__name__)

def afficher_instructions():
    print("Commandes disponibles dans la fenêtre 3D :")
    print("- 'c' : Tracer un carré (100 unités)")
    print("- 'a' : Avancer (100 unités)")
    print("- 'r' : Mode automatique (vitesses 14, 7)")
    print("- 'm' : S'approcher à 5 mm d'un mur/obstacle")
    print("- 'b' : Suivre la balise")
    print("- 'k' : Contrôle par clavier (i pour avancer, o pour reculer, p pour gauche, l pour droite)")
    print("- 't' : Tourner d’un angle spécifié (en degrés)")  # New option
    print("- 'q' : Arrêter la stratégie en cours")
    print("- 'ESC' : Quitter")
    print("- 'UP/DOWN' : Zoom avant/arrière")
    print("- 'LEFT/RIGHT' : Vue à gauche/droite")
    print("===================")

def gerer_touches(affichage3d):
    """Configure la gestion des touches pour l'interface 3D."""
    affichage3d.key_map = {'i': False, 'o': False, 'p': False, 'l': False}
    affichage3d.current_strategy = None

    def handle_key_press(key, value):
        """Handle key press, directing to robot or camera based on strategy."""
        if affichage3d.current_strategy == "clavier" and key in affichage3d.key_map:
            affichage3d.key_map[key] = value
            if isinstance(affichage3d.controleur.strategie, StrategieClavier):
                affichage3d.controleur.strategie.key_map = affichage3d.key_map
                affichage3d.controleur.strategie.step(affichage3d.adaptateur)
                logger.debug(f"Clavier mode - Key '{key}' = {value}, step executed, key_map: {affichage3d.key_map}")
            else:
                logger.warning("Stratégie active n'est pas StrategieClavier")
        elif value and affichage3d.current_strategy != "clavier":
            if key == 'arrow_up':
                affichage3d.changer_mode_camera(1)
                logger.debug("Camera zoom in")
            elif key == 'arrow_down':
                affichage3d.changer_mode_camera(-1)
                logger.debug("Camera zoom out")
            elif key == 'arrow_left':
                affichage3d.changer_lateral_view("left")
                logger.debug("Camera view left")
            elif key == 'arrow_right':
                affichage3d.changer_lateral_view("right")
                logger.debug("Camera view right")

    def stop_strategy():
        """Stop the current strategy."""
        if affichage3d.controleur:
            affichage3d.controleur.stop()
            affichage3d.current_strategy = None
            affichage3d.key_map.update({'i': False, 'o': False, 'p': False, 'l': False})
            logger.info("Stratégie arrêtée par 'q'")
            if affichage3d.taskMgr.hasTaskNamed("update_clavier"):
                affichage3d.taskMgr.remove("update_clavier")
                logger.debug("Tâche update_clavier supprimée")

    def update_clavier_task(task):
        """Task to update StrategieClavier in the Panda3D loop."""
        if affichage3d.current_strategy == "clavier" and affichage3d.controleur and affichage3d.controleur.running:
            if isinstance(affichage3d.controleur.strategie, StrategieClavier):
                affichage3d.controleur.strategie.step(affichage3d.adaptateur)
                logger.debug("update_clavier_task: step exécuté")
            else:
                logger.warning("Stratégie active n'est pas StrategieClavier")
        else:
            logger.debug(f"update_clavier_task: non exécuté (running={affichage3d.controleur.running if affichage3d.controleur else False}, current_strategy={affichage3d.current_strategy})")
        return Task.cont

    affichage3d.accept("escape", affichage3d.quitter)
    affichage3d.accept("q", stop_strategy)
    affichage3d.accept("c", lancer_strategie, [affichage3d, "tracer_carre"])
    affichage3d.accept("a", lancer_strategie, [affichage3d, "avancer"])
    affichage3d.accept("r", lancer_strategie, [affichage3d, "auto"])
    affichage3d.accept("m", lancer_strategie, [affichage3d, "arret_mur"])
    affichage3d.accept("b", lancer_strategie, [affichage3d, "suivre_balise"])
    affichage3d.accept("k", lancer_strategie, [affichage3d, "clavier"])
    affichage3d.accept("t", lancer_strategie, [affichage3d, "tourner"])  # New key binding
    affichage3d.accept("i", handle_key_press, ['i', True])
    affichage3d.accept("o", handle_key_press, ['o', True])
    affichage3d.accept("p", handle_key_press, ['p', True])
    affichage3d.accept("l", handle_key_press, ['l', True])
    affichage3d.accept("i-up", handle_key_press, ['i', False])
    affichage3d.accept("o-up", handle_key_press, ['o', False])
    affichage3d.accept("p-up", handle_key_press, ['p', False])
    affichage3d.accept("l-up", handle_key_press, ['l', False])
    affichage3d.accept("arrow_up", handle_key_press, ['arrow_up', True])
    affichage3d.accept("arrow_down", handle_key_press, ['arrow_down', True])
    affichage3d.accept("arrow_left", handle_key_press, ['arrow_left', True])
    affichage3d.accept("arrow_right", handle_key_press, ['arrow_right', True])
    affichage3d.accept("arrow_up-up", handle_key_press, ['arrow_up', False])
    affichage3d.accept("arrow_down-up", handle_key_press, ['arrow_down', False])
    affichage3d.accept("arrow_left-up", handle_key_press, ['arrow_left', False])
    affichage3d.accept("arrow_right-up", handle_key_press, ['arrow_right', False])

    affichage3d.accept("mouse1", affichage3d.createBalise, [None])
    logger.debug("Gestion des touches configurée dans menu3d")

def lancer_strategie(affichage3d, strategie_type):
    """Lance une stratégie via le contrôleur ou gère la visibilité de la balise."""
    if affichage3d.controleur is None:
        logger.error("Contrôleur non défini, impossible de lancer la stratégie")
        return
    if affichage3d.adaptateur is None:
        logger.error("Adaptateur non défini, impossible de lancer la stratégie")
        return
    try:
        if affichage3d.controleur and affichage3d.current_strategy:
            affichage3d.controleur.stop()
            if affichage3d.taskMgr.hasTaskNamed("update_clavier"):
                affichage3d.taskMgr.remove("update_clavier")
                logger.debug("Tâche update_clavier supprimée avant nouvelle stratégie")
            logger.info(f"Stratégie précédente '{affichage3d.current_strategy}' arrêtée")

        affichage3d.current_strategy = strategie_type

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
                affichage3d.showBalise = True
                if not affichage3d.balise and affichage3d.robot:
                    cos_a, sin_a = affichage3d.robot.direction[0], affichage3d.robot.direction[1]
                    distance_from_robot = 100
                    beacon_x = affichage3d.robot.x + cos_a * distance_from_robot
                    beacon_y = affichage3d.robot.y + sin_a * distance_from_robot
                    beacon_x = max(0, min(affichage3d.largeur, beacon_x))
                    beacon_y = max(0, min(affichage3d.hauteur, beacon_y))
                    affichage3d.beacon_position = [beacon_x, beacon_y]
                    from src.interface_graphique.interface3D.interface3d import Balise
                    affichage3d.balise = Balise(beacon_x, beacon_y, 40, 30)
                affichage3d.fixed_beacon = True
                logger.info("Balise affichée")
                affichage3d.controleur.set_strategie("suivre_balise", adaptateur=affichage3d.adaptateur)
            else:
                affichage3d.showBalise = False
                affichage3d.fixed_beacon = False
                if affichage3d.balise_node:
                    affichage3d.balise_node.removeNode()
                    affichage3d.balise_node = None
                if affichage3d.balise:
                    affichage3d.balise = None
                logger.info("Balise cachée")
                affichage3d.current_strategy = None
                return
        elif strategie_type == "clavier":
            affichage3d.key_map.update({'i': False, 'o': False, 'p': False, 'l': False})
            affichage3d.controleur.set_strategie("clavier", adaptateur=affichage3d.adaptateur, key_map=affichage3d.key_map)
            affichage3d.taskMgr.add(update_clavier_task, "update_clavier")
            logger.info("Mode contrôle par clavier lancé avec update task")
        elif strategie_type == "tourner":
            try:
                # Panda3D doesn't support console input, so we prompt via print/input
                print("Entrez l’angle de rotation en degrés (positif pour gauche, négatif pour droite) : ")
                angle = float(input())  # Note: This blocks the Panda3D loop; consider GUI input in production
                if not -360 <= angle <= 360:
                    raise ValueError("L’angle doit être entre -360 et 360 degrés")
                affichage3d.controleur.set_strategie(StrategieTourner, angle=angle)
                logger.info(f"Stratégie 'tourner' lancée avec angle={angle}")
            except ValueError as e:
                logger.error(f"Erreur lors de la saisie de l’angle : {e}")
                print(f"Erreur : {e}")
                affichage3d.current_strategy = None
                return
        affichage3d.controleur.lancerStrategie()
        logger.info(f"Stratégie '{strategie_type}' lancée")
    except Exception as e:
        logger.error(f"Erreur lors du lancement de la stratégie {strategie_type}: {e}")