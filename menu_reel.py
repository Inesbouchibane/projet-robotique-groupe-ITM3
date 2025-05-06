from src.controleur.strategies import StrategieAvancer, setStrategieCarre, 
StrategieArretMur, StrategieSuivreBalise
from time import sleep

def afficher_menu():
    """Affiche le menu dans la console"""
    print("=== Menu Mockup ===")
    print("Commandes disponibles :")
    print("  a - J'avance de 100 mm")
    print("  c - Je dessine un carré de 100 mm par côté")
    print("  m - Je m'approche à 5 mm d'un mur")
    print("  b - Je suis la balise avec la caméra")
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
        print("J’ai préparé ma stratégie d’approche")
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
        print("Je reste immobile et j’attends un nouveau choix")

    return True
