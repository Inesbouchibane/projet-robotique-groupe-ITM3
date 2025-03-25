from robot.robot_mockup import RobotMockup
from robot.adapt.Adaptateur_simule import Adaptateur_simule
from environnement.balise import Balise
from controleur.strategies import StrategieSuivreBalise
from interface_graphique import Affichage
from time import sleep
from utils import TIC_SIMULATION, LARGEUR_ENV, LONGUEUR_ENV

def main():
    # Initialisation du robot
    robot = RobotMockup("MockBot", 400, 300, 20, 40, 10, 5, "red")
    adaptateur = Adaptateur_simule(robot, None)  # Pas d'environnement pour ce test
    balise = Balise(600, 400)  # Balise à (600, 400)
    strategie = StrategieSuivreBalise(adaptateur, balise)
    
     # Initialisation de l'affichage
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, [])

    print("Test de la stratégie Suivre Balise")
    strategie.start()

    
    running = True
    while running:
        strategie.step()
        if strategie.running:  # Ne refresh que si la stratégie est active
            robot.refresh(TIC_SIMULATION)
            affichage.mettre_a_jour(robot)
            
            
        # Gestion des événements pour quitter
        action = affichage.handle_events(adaptateur)
        if action == "quit":
            strategie.stop()
            running = False

        sleep(TIC_SIMULATION)

    affichage.attendre_fermeture()




