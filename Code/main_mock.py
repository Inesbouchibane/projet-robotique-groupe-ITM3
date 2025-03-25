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
        
        try:
            if choix == "1":
                vitesse = float(input("Entrez la vitesse angulaire (ex. 10) : "))
                robot.setVitAng(vitesse)
                print(f"Avance avec vitesse {vitesse}")
            elif choix == "2":
                vitesse = float(input("Entrez la vitesse de rotation (ex. 10) : "))
                robot.vitAngG = vitesse
                robot.vitAngD = -vitesse / 2
                print(f"Tourne à gauche : vitG = {vitesse}, vitD = {-vitesse / 2}")
            elif choix == "3":
                vitesse = float(input("Entrez la vitesse de rotation (ex. 10) : "))
                robot.vitAngG = -vitesse / 2
                robot.vitAngD = vitesse
                print(f"Tourne à droite : vitG = {-vitesse / 2}, vitD = {vitesse}")
            elif choix == "4":
                robot.setVitAng(0)
                print("Robot arrêté")
            elif choix == "5":
                print("Au revoir !")
                running = False
            else:
                print("Choix invalide, essayez encore.")
                
            # Si le robot bouge, met à jour sa position
            if choix in ["1", "2", "3"]:
                for _ in range(10):  # Simule 1 seconde (10 x 0.1s)
                    robot.refresh(0.1)
                    print(f"Position : ({robot.x:.2f}, {robot.y:.2f}), Direction : {robot.direction}")
                    sleep(0.1)
                    
                    
         except ValueError:
            print("Erreur : Entrez une valeur numérique valide pour la vitesse.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    main()
