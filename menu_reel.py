from src.controleur.strategies import StrategieAvancer, setStrategieCarre, StrategieArretMur, StrategieSuivreBalise, StrategieClavier, StrategieTourner  # Add StrategieTourner
from src.utils import TIC_CONTROLEUR
from time import sleep
import keyboard
import math as m
from logging import getLogger

logger = getLogger(__name__)

def afficher_menu():
    """Affiche le menu dans la console"""
    print("=== Menu Mockup ===")
    print("Commandes disponibles :")
    print("  a - J'avance de 100 mm")
    print("  c - Je dessine un carré de 100 mm par côté")
    print("  m - Je m'approche à 5 mm d'un mur")
    print("  b - Je suis la balise avec la caméra")
    print("  k - Contrôle par clavier (i pour avancer, o pour reculer, p pour tourner à gauche, l pour tourner à droite)")
    print("  t - Tourner d’un angle spécifié (en degrés)")  # New option
    print("  q - Je m'arrête")
    print("===================")

def gerer_choix(controleur, choix, logger):
    adaptateur = controleur.adaptateur

    if choix == 'a':
        logger.info("Choix 'a' - Je vais avancer de 100 mm")
        print("Je décide d’avancer de 100 mm")
        print("Je crée une stratégie pour avancer de 100 mm")
        strategie = StrategieAvancer(100)
        print("J’ai préparé ma stratégie d’avancement")
        adaptateur.initialise()
        controleur.lancerStrategie(strategie)
        print("Je démarre l’exécution de ma stratégie d’avancement")
        print("Je surveille chaque étape de mon avancement")

        dernier_affichage = 0
        while controleur.running:
            distance_parcourue = adaptateur.getDistanceParcourue()
            distance_obstacle = adaptateur.getDistanceA()
            distance_entier = int(distance_parcourue)
            if distance_entier > dernier_affichage and distance_entier <= 100:
                print(f"J’avance : {distance_entier} mm parcourus, distance à l'obstacle : {distance_obstacle:.2f} mm")
                dernier_affichage = distance_entier
            sleep(0.01)
        print("J’ai détecté que la stratégie est terminée")
        print("J’ai fini d’avancer de 100 mm")
        print("Je suis prêt pour une nouvelle action")

    elif choix == 'c':
        logger.info("Choix 'c' - Je vais dessiner un carré")
        print("Je décide de dessiner un carré de 100 mm par côté")
        print("Je crée une stratégie pour dessiner mon carré")
        strategie = setStrategieCarre(100)
        print("J’ai préparé ma stratégie pour le carré")
        adaptateur.initialise()
        controleur.lancerStrategie(strategie)
        print("Je démarre l’exécution de ma stratégie de carré")
        print("Je surveille chaque étape de mon dessin")

        for cote in range(1, 5):
            print(f"Je commence le côté {cote} du carré")
            dernier_affichage = 0
            distance_depart = adaptateur.getDistanceParcourue()
            while controleur.running:
                distance_parcourue_totale = adaptateur.getDistanceParcourue()
                distance_obstacle = adaptateur.getDistanceA()
                distance_cote = distance_parcourue_totale - distance_depart
                distance_entier = int(distance_cote)
                if distance_entier > dernier_affichage and distance_entier <= 100:
                    print(f"Côté {cote} : {distance_entier} mm parcourus, distance à l'obstacle : {distance_obstacle:.2f} mm")
                    dernier_affichage = distance_entier
                sleep(0.01)
                if distance_entier >= 100:
                    break
            if not controleur.running:
                break
            print(f"J’ai fini le côté {cote} du carré")

        print("J’ai détecté que la stratégie est terminée")
        print("J’ai fini de dessiner mon carré")
        print("Je suis prêt pour une nouvelle action")

    elif choix == 'm':
        logger.info("Choix 'm' - Je m'approche à 5 mm d'un mur")
        print("Je décide de m’approcher à 5 mm d’un mur")
        print("Je crée une stratégie pour m’approcher du mur")
        strategie = StrategieArretMur(adaptateur, distance_arret=5)
        print("J’ai préparé ma stratégie d’appro Approach")
        adaptateur.initialise()
        controleur.lancerStrategie(strategie)
        print("Je démarre l’exécution de ma stratégie d’approche")
        print("Je surveille la distance au mur")

        dernier_affichage = 0
        while controleur.running:
            distance_obstacle = adaptateur.getDistanceA()
            distance_entier = int(distance_obstacle)
            if distance_entier < dernier_affichage or dernier_affichage == 0:
                print(f"Distance au mur : {distance_entier} mm")
                dernier_affichage = distance_entier
            sleep(0.01)
        print("J’ai détecté que la stratégie est terminée")
        print("J’ai fini de m’approcher du mur")
        print("Je suis prêt pour une nouvelle action")

    elif choix == 'b':
        logger.info("Choix 'b' - Je vais suivre la balise")
        print("Je décide de suivre la balise")
        print("Je crée une stratégie pour suivre la balise")
        strategie = StrategieSuivreBalise(adaptateur)
        print("J’ai préparé ma stratégie de suivi")
        adaptateur.initialise()
        controleur.lancerStrategie(strategie)
        print("Je démarre l’exécution de ma stratégie de suivi")
        print("Je surveille la balise avec la caméra")

        while controleur.running:
            strategie.step(adaptateur)
            distance_obstacle = adaptateur.getDistanceA()
            print(f"Suivi de la balise, distance à l'obstacle : {distance_obstacle:.2f} mm")
            if strategie.stop(adaptateur):
                print("J’ai détecté que la stratégie est terminée")
                break
            sleep(0.01)
        print("J’ai fini de suivre la balise")
        print("Je suis prêt pour une nouvelle action")

    elif choix == 'k':
        logger.info("Choix 'k' - Contrôle par clavier")
        print("Je décide de passer en mode contrôle par clavier")
        print("Utilisez i (avancer), o (reculer), p (gauche), l (droite), q (arrêter)")
        key_map = {'i': False, 'o': False, 'p': False, 'l': False}
        strategie = StrategieClavier(adaptateur, key_map)
        adaptateur.initialise()
        controleur.lancerStrategie(strategie)
        print("Mode clavier activé")

        while controleur.running:
            key_map['i'] = keyboard.is_pressed('i')
            key_map['o'] = keyboard.is_pressed('o')
            key_map['p'] = keyboard.is_pressed('p')
            key_map['l'] = keyboard.is_pressed('l')
            strategie.key_map = key_map
            strategie.step(adaptateur)
            # Fallback: Manually update position
            try:
                if key_map.get('i', False) or key_map.get('o', False):
                    robot = adaptateur.robot
                    linear_vel = VIT_ANG_AVAN if key_map.get('i', False) else -VIT_ANG_AVAN
                    angle = m.atan2(robot.direction[1], robot.direction[0])
                    dx = linear_vel * m.cos(angle) * TIC_CONTROLEUR
                    dy = linear_vel * m.sin(angle) * TIC_CONTROLEUR
                    robot.x += dx
                    robot.y += dy
                    logger.debug(f"Mockup position update: dx={dx:.2f}, dy={dy:.2f}, new_pos=({robot.x:.2f}, {robot.y:.2f})")
            except Exception as e:
                logger.error(f"Erreur lors de la mise à jour de la position: {e}")
            if keyboard.is_pressed('q'):
                controleur.stop()
                adaptateur.cleanup()
                print("Mode clavier arrêté")
                break
            logger.debug(f"État des touches : {key_map}")
            sleep(0.01)
        print("J’ai fini le mode clavier")
        print("Je suis prêt pour une nouvelle action")

    elif choix == 't':
        logger.info("Choix 't' - Je vais tourner d’un angle spécifié")
        print("Je décide de tourner d’un angle spécifié")
        try:
            angle = float(input("Entrez l’angle de rotation en degrés (positif pour gauche, négatif pour droite) : "))
            if not -360 <= angle <= 360:
                raise ValueError("L’angle doit être entre -360 et 360 degrés")
            print(f"Je crée une stratégie pour tourner de {angle} degrés")
            strategie = StrategieTourner(angle)
            print("J’ai préparé ma stratégie de rotation")
            adaptateur.initialise()
            controleur.lancerStrategie(strategie)
            print("Je démarre l’exécution de ma stratégie de rotation")
            print("Je surveille l’angle parcouru")

            dernier_affichage = 0
            while controleur.running:
                angle_parcouru = adaptateur.getAngleParcouru()
                angle_entier = int(angle_parcouru)
                if angle_entier > dernier_affichage or angle_entier < dernier_affichage:
                    print(f"Rotation : {angle_parcouru:.2f} degrés parcourus")
                    dernier_affichage = angle_entier
                sleep(0.01)
            print("J’ai détecté que la stratégie est terminée")
            print(f"J’ai fini de tourner de {angle} degrés")
            print("Je suis prêt pour une nouvelle action")
        except ValueError as e:
            logger.error(f"Erreur lors de la saisie de l’angle : {e}")
            print(f"Erreur : {e}")
            print("Je reste immobile et j’attends un nouveau choix")

    elif choix == 'q':
        logger.info("Je m’arrête")
        print("Je décide de tout arrêter")
        controleur.stop()
        adaptateur.cleanup()
        print("J’ai envoyé l’ordre d’arrêt")
        print("Je mets fin à toutes mes actions")
        return False

    else:
        print("Je détecte un choix invalide")
        logger.warning("Invalid choice entered")
        print("Je reste immobile et j’attends un nouveau choix")

    return True