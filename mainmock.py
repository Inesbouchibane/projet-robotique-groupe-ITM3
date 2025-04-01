from src.robot.adapt_reel import Adaptateur_reel
from src.robot.robot_mockup import MockupRobot
from menu import choisir_strategie
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO)

# Initialisation du robot et de l'adaptateur
robot = MockupRobot()
adaptateur = Adaptateur_reel(robot)

def main():
    controleur = None  # Pas utilisé dans le mockup, mais requis par menu.py
    choisir_strategie(controleur, adaptateur, type_simulation="mockup")
    print("Simulation terminée.")

if __name__ == "__main__":
    main()
