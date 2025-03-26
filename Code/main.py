# main.py
from threading import Thread
from time import sleep
from robot.robot import Robot
from robot.adapt import Adaptateur_simule
from environnement.environnement import Environnement
from affichage import Affichage
from controleur.controleur import Controler
from controleur.strategies import setStrategieCarre, StrategieAuto, StrategieVersMur  # Ajout de la nouvelle stratégie
from utils import TIC_SIMULATION, LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1, LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_CARRE, LIST_PTS_OBS_RECTANGLE3
from logging import basicConfig, INFO

basicConfig(level=INFO)

envi = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
robot1 = Robot("r1", 500, 250, 20, 40, 10, 5, "lightblue")
adaptateur = Adaptateur_simule(robot1, envi)
envi.setRobot(adaptateur)

for n, pts in [('R1', LIST_PTS_OBS_RECTANGLE1), ('R2', LIST_PTS_OBS_CARRE), ('R3', LIST_PTS_OBS_RECTANGLE3)]:
    envi.addObstacle(n, pts)

affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, [o.get_bounding_box() for o in envi.listeObs])

def loopEnv(envi):
    while True:
        envi.refreshEnvironnement()
        sleep(TIC_SIMULATION)

def main_loop():
    controleur = Controler()
    running = True

    print("Choisissez une stratégie :")
    print("1. Tracer un carré (touche 'c')")
    print("2. Mode automatique (touche 'a')")
    print("3. Avancer vers le mur le plus proche")  # Nouvelle option
    strategy_choice = input("Entrez 1, 2 ou 3 : ").strip()

    if strategy_choice == "1":
        longueur_cote = float(input("Entrez la longueur du côté du carré : "))
        strat_carre = setStrategieCarre(adaptateur, longueur_cote)
        controleur.lancerStrategie(strat_carre)
        print("Stratégie 'tracer_carre' lancée. Appuyez sur ESC pour quitter.")
    elif strategy_choice == "2":
        vitAngG = float(input("Entrez la vitesse angulaire de la roue gauche (vitAngG) : "))
        vitAngD = float(input("Entrez la vitesse angulaire de la roue droite (vitAngD) : "))
        strat_auto = StrategieAuto(adaptateur, vitAngG, vitAngD)
        controleur.lancerStrategie(strat_auto)
        print("Stratégie 'automatique' lancée. Appuyez sur ESC pour quitter.")
    elif strategy_choice == "3":  # Gestion de la nouvelle stratégie
        strat_vers_mur = StrategieVersMur(adaptateur)
        controleur.lancerStrategie(strat_vers_mur)
        print("Stratégie 'vers mur' lancée. Appuyez sur ESC pour quitter.")
    else:
        print("Choix invalide. Démarrage sans stratégie prédéfinie.")

    while running:
        action = affichage.handle_events(adaptateur)
        if action == "quit":
            running = False
        elif action == "tracer_carre":
            longueur_cote = float(input("Entrez la longueur du côté du carré : "))
            strat_carre = setStrategieCarre(adaptateur, longueur_cote)
            controleur.lancerStrategie(strat_carre)
            print("Stratégie 'tracer_carre' relancée.")
        elif action == "automatique":
            vitAngG = float(input("Entrez la vitesse angulaire de la roue gauche (vitAngG) : "))
            vitAngD = float(input("Entrez la vitesse angulaire de la roue droite (vitAngD) : "))
            strat_auto = StrategieAuto(adaptateur, vitAngG, vitAngD)
            controleur.lancerStrategie(strat_auto)
            print("Stratégie 'automatique' relancée.")

        affichage.mettre_a_jour(robot1)
        sleep(TIC_SIMULATION)

    affichage.attendre_fermeture()

if __name__ == "__main__":
    Thread(target=loopEnv, args=(envi,), daemon=True).start()
    main_loop()
