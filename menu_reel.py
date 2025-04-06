from src.controleur.strategies import StrategieAvancer, setStrategieCarre
from time import sleep

def afficher_menu():
    """Affiche le menu dans la console"""
    print("=== Menu Mockup ===")
    print("Commandes disponibles :")
    print("  a - J'avance de 100 mm")
    print("  c - Je dessine un carré de 100 mm par côté")
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
            distance_entier = int(distance_parcourue)
            if distance_entier > dernier_affichage and distance_entier <= 100:
                print(f"J’avance : {distance_entier} mm parcourus")
                dernier_affichage = distance_entier
            sleep(0.01)  # Vérification fréquente
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
                distance_cote = distance_parcourue_totale - distance_depart
                distance_entier = int(distance_cote)
                if distance_entier > dernier_affichage and distance_entier <= 100:
                    print(f"Côté {cote} : {distance_entier} mm parcourus")
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

    elif choix == 'q':
        logger.info("Je m’arrête")
        print("Je décide de tout arrêter")
        controleur.stop()
        print("J’ai envoyé l’ordre d’arrêt")
        print("Je mets fin à toutes mes actions")
        return False

    else:
        print("Je détecte un choix invalide")
        print("Je reste immobile et j’attends un nouveau choix")

    return True