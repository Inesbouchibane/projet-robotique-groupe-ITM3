from robot.robot_mockup import RobotMockup
from time import sleep

def main():
    # Initialisation du robot mockup
    robot = RobotMockup(
        nom="MockBot",
        x=0,          # Position initiale x
        y=0,          # Position initiale y
        width=20,     # Largeur
        length=40,    # Longueur
        height=10,    # Hauteur (non utilisé ici)
        rayonRoue=5,  # Rayon des roues
        couleur="red" # Couleur (non utilisé ici)
    )
 
    print("Bienvenue dans le test de RobotMockup !")
    print(f"Position initiale : ({robot.x:.2f}, {robot.y:.2f})")
    print(f"Direction initiale : {robot.direction}")
    
    # Boucle principale
    running = True
    while running:
        print("\nMenu :")
        print("1. Avancer tout droit")
        print("2. Tourner à gauche")
        print("3. Tourner à droite")
        print("4. Arrêter le robot")
        print("5. Quitter")
        choix = input("Entrez votre choix (1-5) : ").strip()
