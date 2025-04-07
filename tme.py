# tme.py
from threading import Thread
from time import sleep, time
from src import (
    RobotSimule, AdaptateurSimule, Environnement, Controler,
    TIC_SIMULATION, LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1,
    LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_TRIANGLE, LIST_PTS_OBS_CERCLE,
    StrategieAvancer, StrategieAuto, setStrategieCarre
)
from src.interface_graphique.interface2D.menu2d import gerer_evenements, 
afficher_instructions
from src.interface_graphique.interface2D.interface2d import Affichage
from logging import basicConfig, INFO, getLogger

basicConfig(level=INFO)
logger = getLogger(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Démarrage du programme")
    afficher_instructions()

    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)

    env.addObstacle("Rectangle", LIST_PTS_OBS_RECTANGLE1)
    env.addObstacle("Triangle ", LIST_PTS_OBS_TRIANGLE)
    env.addObstacle("Cercle", LIST_PTS_OBS_CERCLE)
    logger.info("Environnement initialisé")

    #On copie le main et modiife les valeurs pr déplacer comme demande 
dans qst1.1   
    robot = RobotSimule("r1", 50, 50, 25, 30, 50, 5,couleur = "red")
    adaptateur = AdaptateurSimule(robot, env)
    env.setRobot(adaptateur)
    logger.info(f"Robot initialisé à ({robot.x}, {robot.y})")
   
    controleur = Controler(adaptateur)
    logger.info("Contrôleur initialisé")

    obstacles = [LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_TRIANGLE, LIST_PTS_OBS_CERCLE]
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, obstacles)
    logger.info("Affichage initialisé")

    

    running = True
    logger.info("Début de la boucle principale")
    while running:
        logger.debug("Appel de gerer_evenements")
        action = gerer_evenements(controleur)
        logger.debug(f"Action reçue : {action}")
        if action == "quit":
            controleur.stop()
            running = False
            logger.info("Arrêt demandé")
        env.refreshEnvironnement()
        affichage.mettre_a_jour(robot)
        sleep(TIC_SIMULATION)

    logger.info("Fin de la boucle principale")
    affichage.attendre_fermeture()
    logger.info("Programme terminé")

if __name__ == "__main__":
    main()
