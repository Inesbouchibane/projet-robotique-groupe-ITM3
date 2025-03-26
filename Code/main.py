from threading import Thread
from time import sleep
from robot.robot import Robot
from robot.adapt.Adaptateur_simule import Adaptateur_simule
from environnement.Environnement import Environnement
from interface_graphique.affichage import Affichage
from controleur.controleur import Controler
from controleur.strategies import setStrategieCarre, StrategieAuto, 
StrategieVersMur
from utils import TIC_SIMULATION, LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1, 
LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_CARRE, LIST_PTS_OBS_RECTANGLE3
from logging import basicConfig, INFO

basicConfig(level=INFO)

envi = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
robot1 = Robot("r1", 500, 250, 20, 40, 10, 5, "lightblue")
adaptateur = Adaptateur_simule(robot1, envi)
envi.setRobot(adaptateur)

for n, pts in [('R1', LIST_PTS_OBS_RECTANGLE1), ('R2', 
LIST_PTS_OBS_CARRE), ('R3', LIST_PTS_OBS_RECTANGLE3)]:
    envi.addObstacle(n, pts)

affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, [o.get_bounding_box() for 
o in envi.listeObs])

def loopEnv(envi):
    while True:
        envi.refreshEnvironnement()
        sleep(TIC_SIMULATION)

def main_loop():
    controleur = Controler()
    running = True

    while running:
        print("Choisissez une stratégie :")
        print("1. Tracer un carré (touche 'c')")
        print("2. Mode automatique (touche 'a')")
        print("3. Avancer vers le mur le plus proche")
        print("Appuyez sur 'q' ou fermez la fenêtre pour quitter")
        strategy_choice = input("Entrez 1, 2 ou 3 (ou 'q' pour quitter) : 
").strip()

        try:
            if strategy_choice == "1":
                longueur_cote = float(input("Entrez la longueur du côté du 
carré : "))
                strat_carre = setStrategieCarre(adaptateur, longueur_cote)
                controleur.lancerStrategie(strat_carre)
                print("Stratégie 'tracer_carre' lancée. Appuyez sur ESC 
pour interrompre...")

                while controleur.strategie:
                    action = affichage.handle_events(adaptateur)
                    if action == "quit" or (action == "automatique" and 
controleur.strategie):
                        controleur.strat_en_cours.running = False
                        controleur.strategie = False
                        print("Stratégie interrompue.")
                        break
                    affichage.mettre_a_jour(robot1)
                    sleep(TIC_SIMULATION)

                print("Stratégie 'tracer_carre' terminée ou interrompue.")

            elif strategy_choice == "2":
                vitAngG = float(input("Entrez la vitesse angulaire de la 
roue gauche (vitAngG) : "))
                vitAngD = float(input("Entrez la vitesse angulaire de la 
roue droite (vitAngD) : "))
                strat_auto = StrategieAuto(adaptateur, vitAngG, vitAngD)
                controleur.lancerStrategie(strat_auto)
                print("Stratégie 'automatique' lancée. Appuyez sur ESC 
pour interrompre...")

                while controleur.strategie:
                    action = affichage.handle_events(adaptateur)
                    if action == "quit" or (action == "automatique" and 
controleur.strategie):
                        controleur.strat_en_cours.running = False
                        controleur.strategie = False
                        adaptateur.setVitAngA(0)
                        print("Stratégie interrompue.")
                        break
                    affichage.mettre_a_jour(robot1)
                    sleep(TIC_SIMULATION)

                print("Stratégie 'automatique' terminée ou interrompue.")

            elif strategy_choice == "3":
                strat_vers_mur = StrategieVersMur(adaptateur)
                controleur.lancerStrategie(strat_vers_mur)
                print("Stratégie 'vers mur' lancée. Appuyez sur ESC pour 
interrompre...")

                while controleur.strategie:
                    action = affichage.handle_events(adaptateur)
                    if action == "quit" or (action == "automatique" and 
controleur.strategie):
                        controleur.strategie = False
                        print("Stratégie interrompue.")
                        break
                    affichage.mettre_a_jour(robot1)
                    sleep(TIC_SIMULATION)

                print("Stratégie 'vers mur' terminée ou interrompue.")

            elif strategy_choice.lower() == "q":
                print("Fermeture du programme...")
                running = False
            else:
                print("Choix invalide. Veuillez réessayer.")
        
        except ValueError:
            print("Erreur : Veuillez entrer une valeur numérique valide.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    affichage.attendre_fermeture()

if __name__ == "__main__":
    Thread(target=loopEnv, args=(envi,), daemon=True).start()
    main_loop()

