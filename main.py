# main.py
import sys
from src.interface_graphique.interface2D.interface2d import Affichage as Affichage2D
from src.interface_graphique.interface3D.interface3d import Affichage3D
from src.utils import *
from src.environnement import Environnement
from src.robot.robot_simule import RobotSimule
from src.controleur.adapt_simule import AdaptateurSimule
from src.controleur.controleur import Controler
from src.interface_graphique.interface2D.menu2d import gerer_evenements as gerer_evenements_2d
from src.interface_graphique.interface3D.menu3d import gerer_evenements as gerer_evenements_3d, afficher_instructions as afficher_instructions_3d
from time import sleep
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialisation commune
    envi = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    obstacles = [LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_TRIANGLE, LIST_PTS_OBS_CERCLE]
    for obs in obstacles:
        envi.addObstacle("obs", obs)
    
    robot = RobotSimule("Robot1", 300, 125, 25, 30, 5, 20)
    adaptateur = AdaptateurSimule(robot, envi)
    controleur = Controler(adaptateur)
    envi.setRobot(adaptateur)

    print("Bienvenue dans le simulateur de robot")
    print("Choisissez le mode d'affichage :")
    print("1. Interface 2D")
    print("2. Interface 3D")
    
    while True:
        choix = input("Entrez votre choix (1 ou 2) : ").strip()
        if choix in ["1", "2"]:
            break
        print("Choix invalide, veuillez entrer 1 ou 2.")

    if choix == "1":
        logger.info("Initialisation de l'interface 2D")
        print("Initialisation 2D...")
        affichage = Affichage2D(LARGEUR_ENV, LONGUEUR_ENV, obstacles)
        
        running = True
        logger.info("Début de la boucle principale 2D")
        while running:
            action = gerer_evenements_2d(controleur)
            if action == "quit":
                controleur.stop()
                running = False
                logger.info("Arrêt de l'interface 2D")
            envi.refreshEnvironnement()
            affichage.mettre_a_jour(robot)
            sleep(TIC_SIMULATION)
            
        affichage.attendre_fermeture()
        logger.info("Fermeture de l'interface 2D")

    elif choix == "2":
        logger.info("Initialisation de l'interface 3D")
        print("Initialisation 3D...")
        afficher_instructions_3d()  # Afficher les instructions spécifiques à l'interface 3D
        affichage = Affichage3D(LARGEUR_ENV, LONGUEUR_ENV, [o.points for o in envi.listeObs])
        
        running = True
        logger.info("Début de la boucle principale 3D")
        while running:
            action = gerer_evenements_3d(controleur)
            if action == "quit":
                controleur.stop()
                running = False
                logger.info("Arrêt de l'interface 3D")
            envi.refreshEnvironnement()
            affichage.mettre_a_jour(robot)
            sleep(TIC_SIMULATION)
            
        affichage.attendre_fermeture()
        logger.info("Fermeture de l'interface 3D")

if __name__ == "__main__":
    main()