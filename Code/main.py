from threading import Thread
from time import sleep
from robot.robot import Robot
from robot.adapt.Adaptateur_simule import Adaptateur_simule
from environnement.Environnement import Environnement
from interface_graphique.affichage import Affichage
from controleur.controleur import Controler
from controleur.strategies import setStrategieCarre, StrategieAuto, StrategieVersMur
from utils import TIC_SIMULATION, LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1, LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_CARRE, LIST_PTS_OBS_RECTANGLE3
from logging import basicConfig, INFO

def main_loop():
    controleur = Controler()
    running = True

    for _ in range(3):  # Demande à l'utilisateur 3 fois
        print("\nChoisissez une stratégie :")
        print("1. Tracer un carré (touche 'c')")
        print("2. Mode automatique (touche 'a')")
        print("3. Avancer vers le mur le plus proche")  # Nouvelle option
        strategy_choice = input("Entrez 1, 2 ou 3 : ").strip()

        if strategy_choice == "1":
            longueur_cote = float(input("Entrez la longueur du côté du carré : "))
            strat_carre = setStrategieCarre(adaptateur, longueur_cote)
            controleur.lancerStrategie(strat_carre)
            print("Stratégie 'tracer_carre' lancée.")
        elif strategy_choice == "2":
            vitAngG = float(input("Entrez la vitesse angulaire de la roue gauche (vitAngG) : "))
            vitAngD = float(input("Entrez la vitesse angulaire de la roue droite (vitAngD) : "))
            strat_auto = StrategieAuto(adaptateur, vitAngG, vitAngD)
            controleur.lancerStrategie(strat_auto)
            print("Stratégie 'automatique' lancée.")
        elif strategy_choice == "3":  
            strat_vers_mur = StrategieVersMur(adaptateur)
            controleur.lancerStrategie(strat_vers_mur)
            print("Stratégie 'vers mur' lancée.")
        else:
            print("Choix invalide. Essayez encore.")

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

