from threading import Thread
from time import sleep, time
from src import (
    RobotSimule, AdaptateurSimule, Environnement, Controler,
    TIC_SIMULATION, LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1,
    LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_CERCLE,
    StrategieAvancer, StrategieAuto, setStrategieCarre, StrategieClavier
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
    env.addObstacle("rectangle", LIST_PTS_OBS_RECTANGLE1)
    env.addObstacle("cercle", LIST_PTS_OBS_CERCLE)
    logger.info("Environnement initialisé")

    robot = RobotSimule("Robot1", 300, 125, 25, 30, 5, 20)  # 100 unités du rectangle
    adaptateur = AdaptateurSimule(robot, env)
    env.setRobot(adaptateur)
    logger.info(f"Robot initialisé à ({robot.x}, {robot.y})")

    controleur = Controler(adaptateur)
    # Initialize key_map for StrategieClavier
    key_map = {'up': False, 'down': False, 'left': False, 'right': False}
    controleur.set_strategie("clavier", adaptateur=adaptateur, key_map=key_map)
    controleur.lancerStrategie()
    logger.info("Contrôleur initialisé avec StrategieClavier par défaut")

    obstacles = [LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_CERCLE]
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, obstacles)
    logger.info("Affichage initialisé")

    running = True
    logger.info("Début de la boucle principale")
    while running:
        logger.debug("Appel de gerer_evenements")
        action = gerer_evenements(controleur, key_map)
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