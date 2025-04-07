from threading import Thread
from time import sleep, time
from src import (
    RobotSimule, AdaptateurSimule, Environnement, Controler,Controlers
    TIC_SIMULATION, LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1,
    LIST_PTS_OBS_Forme1,LIST_PTS_OBS_Forme2,LIST_PTS_OBS_Forme3,
    StrategieAvancer, StrategieAuto, setStrategieCarre
)
from src.interface_graphique.interface2D.menu2d import gerer_evenements, afficher_instructions
from src.interface_graphique.interface2D.interface2d import Affichage
from logging import basicConfig, INFO, getLogger

basicConfig(level=INFO)
logger = getLogger(__name__)

def main():
    logger.info("Démarrage du programme")
    afficher_instructions()

    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    env.addObstacle("forme1", [(450,150), (550, 150), (450, 350), (100,450 )])
    env.addObstacle("forme2", [(450, 200), (550, 150), (450, 175)])
    env.addObstacle("forme3", [(420, 150), (300, 100), (325, 150)])
    logger.info("Environnement initialisé")

    robot = RobotSimule("Robot1", 300, 125, 25, 30, 5, 20)  # 100 unités du rectangle
    robot2=RobotSimule("Robot2", 320, 145, 45, 70, 25, 40)
    adaptateur = AdaptateurSimule(robot, env)
    adaptateur2 = AdaptateurSimule(robot2, env)
    env.setRobot(adaptateur)
    env.setRobot(adaptateur2)
    logger.info(f"Robot initialisé à ({robot.x}, {robot.y})")
    logger.info(f"Robot initialisé à ({robot.x}, {robot.y})")
    controleur = Controler(adaptateur)
    controleur2 = Controlers(adaptateur2)
    
    logger.info("Contrôleur initialisé")

    obstacles = [LIST_PTS_OBS_Forme1,LIST_PTS_OBS_Forme2,LIST_PTS_OBS_Forme3]
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, obstacles)
    logger.info("Affichage initialisé")

    running = True
    logger.info("Début de la boucle principale")
    while running:
        logger.debug("Appel de gerer_evenements")
        action = gerer_evenements(controleur)
        action = gerer_evenements(controleur2)
        logger.debug(f"Action reçue : {action}")
        if action == "quit":
            controleur.stop()
            running = False
            logger.info("Arrêt demandé")
        env.refreshEnvironnement()
        affichage.mettre_a_jour(robot)
        affichage.mettre_a_jour(robot2)
        sleep(TIC_SIMULATION)

    logger.info("Fin de la boucle principale")
    affichage.attendre_fermeture()
    logger.info("Programme terminé")

if __name__ == "__main__":
    main()
