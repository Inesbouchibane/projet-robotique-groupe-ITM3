from src.controleur.adapt_reel import Adaptateur_reel
from src.robot.robot_mockup import MockupRobot
from src.controleur.controleur import Controler
import logging
from menu_reel import afficher_menu, gerer_choix  # Importation correcte

# Configuration des logs
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialisation du robot et de l'adaptateur
robot = MockupRobot()
adaptateur = Adaptateur_reel(robot)

def main():
    logger.info("Je démarre le programme")
    print("Je prépare le contrôleur pour gérer toutes mes actions")
    controleur = Controler(adaptateur)
    print("J’ai créé le contrôleur, je suis prêt à commencer")
    running = True

    while running:
        afficher_menu()
        choix = input("Entrez votre choix (a, c, q) : ").strip().lower()
        running = gerer_choix(controleur, choix, logger)

    logger.info("J’ai fini la simulation.")
    print("J’ai terminé toutes mes tâches")
    print("Je ferme la simulation")
    print("Simulation terminée.")

if __name__ == "__main__":
    main()