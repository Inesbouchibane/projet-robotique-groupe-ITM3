from threading import Thread
from time import sleep, time
from src import (
    RobotSimule, AdaptateurSimule, Environnement, Controler,
    TIC_SIMULATION, LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1,
    LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_TRIANGLE, LIST_PTS_OBS_CERCLE,
    StrategieAvancer, StrategieAuto, setStrategieCarre
)
from src.interface_graphique.interface2D.menu2d import gerer_evenements, afficher_instructions
from src.interface_graphique.interface2D.interface2d import Affichage
from logging import basicConfig, INFO, getLogger
from src.controleur.strategies import StrategieCoinDroit


basicConfig(level=INFO)
logger = getLogger(__name__)


largeur = 800  
longueur = 600  


def main():
    logger.info("Démarrage du programme")
    afficher_instructions()

    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    env.addObstacle("rectangle", LIST_PTS_OBS_RECTANGLE1)
    env.addObstacle("triangle", LIST_PTS_OBS_TRIANGLE)
    env.addObstacle("cercle", LIST_PTS_OBS_CERCLE)

    logger.info("Environnement initialisé")

    robot = RobotSimule("souris", 0, 0, 25, 30, 5, 20)  # 100 unités du rectangle
    adaptateur = AdaptateurSimule(robot, env)
    env.setRobot(adaptateur)
    logger.info(f"Robot initialisé à ({robot.x}, {robot.y})")
    controleur = Controler(adaptateur)
    logger.info("Contrôleur initialisé")

    # deuxième robot
    robot2 = RobotSimule("chat", 0, 50, 25, 30, 5, 20) 
    adaptateur2 = AdaptateurSimule(robot2, env)
    env.setRobot(adaptateur2)
    controleur2 = Controler(adaptateur2)
    logger.info(f"Robot 2 initialisé à ({robot2.x}, {robot2.y})")


    obstacles = [LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_TRIANGLE, LIST_PTS_OBS_CERCLE]
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, obstacles)
    logger.info("Affichage initialisé")

    strategie = StrategieCoinDroit(largeur, longueur)
    strategie.start(adaptateur)
    while not strategie.stop(adaptateur):
        strategie.step(adaptateur)


    robot.dessine(True)
    robot2.dessine(True)
    robot.bleu()  #  dessiner en bleu
    robot2.rouge()  # dessiner en rouge
    robot.move(10, 0) 


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

        action2 = gerer_evenements(controleur2)
    if action2 == "quit":
        controleur2.stop()
        running = False
        logger.info("Arrêt deuxième robot")
    affichage.mettre_a_jour(robot2)

    

    logger.info("Fin de la boucle principale")
    affichage.attendre_fermeture()
    logger.info("Programme terminé")

if __name__ == "__main__":
    main()

