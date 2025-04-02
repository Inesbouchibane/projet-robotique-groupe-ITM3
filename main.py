from threading import Thread
from time import sleep, time
from src.robot.robot_simule import RobotSimule
from src.robot.adapt_simule import AdaptateurSimule
from src.environnement import Environnement
from src.interface_graphique.interface2D.affichage import Affichage
from src.controleur.controleur import Controler
from menu import choisir_strategie, relancer_strategie
from src.utils import TIC_SIMULATION, LARGEUR_ENV, LONGUEUR_ENV, 
SCALE_ENV_1, LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_TRIANGLE, LIST_PTS_OBS_CERCLE
from logging import basicConfig, INFO

basicConfig(level=INFO)

# Initialisation de l'environnement et du robot
envi = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
robot_sim = RobotSimule("r1", 500, 250, 23, 40, 50, 5, "lightblue")  # 
vitesse_max = 50
adaptateur = AdaptateurSimule(robot_sim, envi)
envi.setRobot(adaptateur)

# Ajout des obstacles avec les nouvelles formes
for n, pts in [('Rectangle', LIST_PTS_OBS_RECTANGLE1), ('Triangle', LIST_PTS_OBS_TRIANGLE), ('Cercle', LIST_PTS_OBS_CERCLE)]:
    envi.addObstacle(n, pts)

affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, [o.points for o in 
envi.listeObs])  # Passer les points bruts

def loopEnv(envi, running_flag):
    last_time = time()
    while running_flag[0]:
        current_time = time()
        delta_t = current_time - last_time
        envi.refreshEnvironnement()
        last_time = current_time
        sleep(max(0, TIC_SIMULATION - delta_t))


def main_loop():
    controleur = Controler(adaptateur)
    running = [True]
    env_thread = Thread(target=loopEnv, args=(envi, running), daemon=True)

    # Lancer le menu initial
    choisir_strategie(controleur, adaptateur, type_simulation="simule")
    env_thread.start()
    last_time = time()

    # Boucle principale
    while running[0]:
        current_time = time()
        delta_t = current_time - last_time
        last_time = current_time

        action = affichage.handle_events(adaptateur)
        if action == "quit":
            running[0] = False
        elif action in ["tracer_carre", "automatique", "suivre_balise"]:
            relancer_strategie(controleur, adaptateur, action, type_simulation="simule")

        affichage.mettre_a_jour(robot_sim)
        sleep(max(0, TIC_SIMULATION - delta_t))

    env_thread.join()  # Attendre la fin du thread
    affichage.attendre_fermeture()

if __name__ == "__main__":
    main_loop()
