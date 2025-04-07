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

basicConfig(level=INFO)
logger = getLogger(__name__)

def main():
    logger.info("Démarrage du programme")
    afficher_instructions()

    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    env.addObstacle("rectangle", LIST_PTS_OBS_RECTANGLE1)
    env.addObstacle("triangle", LIST_PTS_OBS_TRIANGLE)
    env.addObstacle("cercle", LIST_PTS_OBS_CERCLE)
    logger.info("Environnement initialisé")

    robot1 = RobotSimule("souris", 300, 125, 25, 30, 5, 20)  # 100 unités 
du rectangle
    adaptateur = AdaptateurSimule(robot1, env)
    env.setRobot(adaptateur)
    logger.info(f"Robot initialisé à ({robot1.x}, {robot1.y})")

    controleur = Controler(adaptateur)
    logger.info("Contrôleur initialisé")
    
   # "Ajout deuxieme robot"
    robot2 = RobotSimule("chat", 400, 200, 25, 30, 5, 20, couleur="red")
    adaptateur2 = AdaptateurSimule(robot2, env)
    logger.info(f"Robot2 initialisé à ({robot2.x}, {robot2.y})")

    controleur = Controler(adaptateur1)
    
    #ajout d'instructions pr pouvoir choisir quel robot faire bouger
    robots = {"1": adaptateur1, "2": adaptateur2}
    robot_actif = "1"
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
       if isinstance (action,str) and action.startswitch ("switch:") :
          robot_actif = action.split (":")[1]
	  controleur.adaptateur = robots[robot_actif]
	  env.setRobot (robots[robot_actif]

        robot1.refresh(TIC_SIMULATION)
        robot2.refresh(TIC_SIMULATION)
        env.refreshEnvironnement()
        affichage.mettre_a_jour(robot1)
	affichage.mettre_a_jour(robot2)
        sleep(TIC_SIMULATION)

    logger.info("Fin de la boucle principale")
    affichage.attendre_fermeture()
    logger.info("Programme terminé")

if __name__ == "__main__":
    main()
