from src.controleur.controleur import Controler
from src.controleur.strategies import setStrategieCarre, StrategieAuto, StrategieSuivreBalise, StrategieAvancer, StrategieTourner
from time import sleep, time
from math import degrees

def choisir_strategie(controleur, adaptateur, type_simulation="simule"):
    """
    Permet de choisir et lancer une stratégie pour le contrôleur avec un menu unifié.
    :param controleur: Instance de Controler
    :param adaptateur: Instance de l'adaptateur (simulé, mockup, etc.)
    :param type_simulation: "simule" ou "mockup" pour adapter le comportement
    :return: Booléen indiquant si une stratégie a été lancée
    """
    print("Choisissez une stratégie :")
    print("1. Tracer un carré")
    print("2. Avancer")
    print("3. Mode automatique")
    print("4. Suivre une balise")
    print("5. Tourner")
    choice = input("Entrez 1, 2, 3, 4 ou 5 : ").strip()

    adaptateur.initialise()  # Réinitialise les compteurs initiaux

    if choice == "1":  # Tracer un carré
        longueur_cote = float(input("Entrez la longueur du côté du carré (cm) : "))
        if type_simulation == "simule":
            strat_carre = setStrategieCarre(longueur_cote)
            controleur.lancerStrategie(strat_carre)
            print("Stratégie 'tracer_carre' lancée. Appuyez sur ESC pour quitter.")
        elif type_simulation == "mockup":
            print("Je vais faire un carré...")
            for i in range(4):
                # Réinitialiser avant chaque mouvement
                adaptateur.initialise()
                start_dist = adaptateur.getDistanceParcourue()
                print(f"J'avance de {longueur_cote} cm (côté {i+1}/4)...")
                adaptateur.setVitAngA(5)  # 5 deg/s
                start_time = time()
                while True:
                    current_dist = adaptateur.getDistanceParcourue()
                    distance_parcourue = (current_dist - start_dist) / 10  # Delta en cm
                    if distance_parcourue >= longueur_cote:
                        adaptateur.setVitAngA(0)
                        break
                    print(f"Je suis en train d'avancer... ({distance_parcourue:.2f}/{longueur_cote} cm)")
                    sleep(0.5)  # Mise à jour toutes les 0.5 secondes
                elapsed_time = time() - start_time
                print(f"J'ai avancé de {longueur_cote} cm en {elapsed_time:.2f} secondes")
                sleep(0.5)
                print(f"Distance totale parcourue : {longueur_cote:.2f} cm")
                sleep(0.5)

                # Réinitialiser avant la rotation
                adaptateur.initialise()
                start_angle = adaptateur.getAngleParcouru()
                print("Je tourne à droite de 90°...")
                adaptateur.setVitAngGA(-5)
                adaptateur.setVitAngDA(5)
                start_time = time()
                while True:
                    current_angle = adaptateur.getAngleParcouru()
                    angle_parcouru = abs(current_angle - start_angle)
                    if angle_parcouru >= 90:
                        adaptateur.setVitAngGA(0)
                        adaptateur.setVitAngDA(0)
                        break
                    print(f"Je suis en train de tourner... ({angle_parcouru:.2f}/90°)")
                    sleep(0.5)
                elapsed_time = time() - start_time
                print(f"J'ai tourné de 90° en {elapsed_time:.2f} secondes")
                sleep(0.5)
                print(f"Angle total parcouru : 90.00°")
                sleep(0.5)
            adaptateur.arreter()
            print("J’ai fini mon carré !")
        return True

    elif choice == "2":  # Avancer
        distance = float(input("Entrez la distance à avancer (cm) : "))
        if type_simulation == "simule":
            strat_avancer = StrategieAvancer(distance)
            controleur.lancerStrategie(strat_avancer)
            print("Stratégie 'avancer' lancée. Appuyez sur ESC pour quitter.")
        elif type_simulation == "mockup":
            print(f"Je vais avancer de {distance} cm...")
            adaptateur.initialise()
            start_dist = adaptateur.getDistanceParcourue()
            adaptateur.setVitAngA(5)  # 5 deg/s
            start_time = time()
            while True:
                current_dist = adaptateur.getDistanceParcourue()
                distance_parcourue = (current_dist - start_dist) / 10  # Delta en cm
                if distance_parcourue >= distance:
                    adaptateur.setVitAngA(0)
                    break
                print(f"Je suis en train d'avancer... ({distance_parcourue:.2f}/{distance} cm)")
                sleep(0.5)
            elapsed_time = time() - start_time
            print(f"J'ai avancé de {distance} cm en {elapsed_time:.2f} secondes")
            sleep(0.5)
            print(f"Distance totale parcourue : {distance:.2f} cm")
            adaptateur.arreter()
            print("J’ai fini d’avancer !")
        return True

    elif choice == "3":  # Mode automatique
        try:
            vitAngG = float(input("Entrez la vitesse angulaire de la roue gauche (deg/s) : "))
            vitAngD = float(input("Entrez la vitesse angulaire de la roue droite (deg/s) : "))
            if type_simulation == "simule":
                strat_auto = StrategieAuto(vitAngG, vitAngD)
                controleur.lancerStrategie(strat_auto)
                print("Stratégie 'automatique' lancée. Appuyez sur ESC pour quitter.")
            elif type_simulation == "mockup":
                adaptateur.setVitAngGA(vitAngG)
                adaptateur.setVitAngDA(vitAngD)
                print(f"Mode automatique lancé avec vitAngG={vitAngG}, vitAngD={vitAngD}. Appuyez sur Ctrl+C pour arrêter.")
                try:
                    last_time = time()
                    while True:
                        current_time = time()
                        delta_t = current_time - last_time
                        angle_change = (vitAngD - vitAngG) * delta_t
                        distance_moved = (vitAngG + vitAngD) / 2 * delta_t * (66.5 * 3.14159 / 360) / 10
                        if vitAngG == vitAngD and vitAngG > 0:
                            print(f"J'avance tout droit de {distance_moved:.2f} cm.")
                        elif vitAngG == vitAngD and vitAngG < 0:
                            print(f"Je recule tout droit de {abs(distance_moved):.2f} cm.")
                        elif vitAngG > 0 and vitAngD < 0:
                            print(f"Je tourne à droite sur place de {abs(angle_change):.2f}°.")
                        elif vitAngG < 0 and vitAngD > 0:
                            print(f"Je tourne à gauche sur place de {abs(angle_change):.2f}°.")
                        elif vitAngG > vitAngD and vitAngG > 0 and vitAngD > 0:
                            print(f"Je tourne légèrement à droite en avançant de {distance_moved:.2f} cm, angle {angle_change:.2f}°.")
                        elif vitAngG < vitAngD and vitAngG > 0 and vitAngD > 0:
                            print(f"Je tourne légèrement à gauche en avançant de {distance_moved:.2f} cm, angle {abs(angle_change):.2f}°.")
                        elif vitAngG < vitAngD and vitAngG < 0 and vitAngD < 0:
                            print(f"Je tourne légèrement à droite en reculant de {abs(distance_moved):.2f} cm, angle {angle_change:.2f}°.")
                        elif vitAngG > vitAngD and vitAngG < 0 and vitAngD < 0:
                            print(f"Je tourne légèrement à gauche en reculant de {abs(distance_moved):.2f} cm, angle {abs(angle_change):.2f}°.")
                        elif vitAngG == 0 and vitAngD > 0:
                            print(f"Je pivote à gauche autour de la roue gauche de {angle_change:.2f}°.")
                        elif vitAngG == 0 and vitAngD < 0:
                            print(f"Je pivote à droite autour de la roue gauche de {abs(angle_change):.2f}°.")
                        elif vitAngD == 0 and vitAngG > 0:
                            print(f"Je pivote à droite autour de la roue droite de {angle_change:.2f}°.")
                        elif vitAngD == 0 and vitAngG < 0:
                            print(f"Je pivote à gauche autour de la roue droite de {abs(angle_change):.2f}°.")
                        elif vitAngG == 0 and vitAngD == 0:
                            print("Je suis arrêté.")
                        else:
                            print(f"Je fais un mouvement personnalisé : distance {distance_moved:.2f} cm, angle {angle_change:.2f}°.")
                        last_time = current_time
                        sleep(1)
                except KeyboardInterrupt:
                    adaptateur.arreter()
                    print("Mode automatique arrêté.")
            return True
        except ValueError:
            print("Erreur : Valeurs invalides.")
            return False

    elif choice == "4":  # Suivre une balise
        balise_x = float(input("Entrez la coordonnée x de la balise (cm) : "))
        balise_y = float(input("Entrez la coordonnée y de la balise (cm) : "))
        if type_simulation == "simule":
            strat_balise = StrategieSuivreBalise((balise_x, balise_y))
            controleur.lancerStrategie(strat_balise)
            print("Stratégie 'suivre balise' lancée. Appuyez sur ESC pour quitter.")
        elif type_simulation == "mockup":
            print(f"Suivi de la balise à ({balise_x}, {balise_y}) cm. Appuyez sur Ctrl+C pour arrêter.")
            try:
                while True:
                    adaptateur.setVitAngA(5)
                    print(f"Je suis en train d'avancer vers la balise... ({adaptateur.getDistanceParcourue() / 10:.2f} cm)")
                    sleep(1)
            except KeyboardInterrupt:
                    adaptateur.arreter()
                    print("Suivi de la balise arrêté.")
            return True

    elif choice == "5":  # Tourner
        angle = float(input("Entrez l'angle de rotation en degrés (positif pour droite, négatif pour gauche) : "))
        if type_simulation == "simule":
            strat_tourner = StrategieTourner(angle)
            controleur.lancerStrategie(strat_tourner)
            print("Stratégie 'tourner' lancée. Appuyez sur ESC pour quitter.")
        elif type_simulation == "mockup":
            print(f"Je vais tourner de {angle}°...")
            adaptateur.initialise()
            start_angle = adaptateur.getAngleParcouru()
            if angle > 0:
                adaptateur.setVitAngGA(-5)  # Tourne à droite
                adaptateur.setVitAngDA(5)
                direction = "droite"
            else:
                adaptateur.setVitAngGA(5)  # Tourne à gauche
                adaptateur.setVitAngDA(-5)
                direction = "gauche"
            start_time = time()
            while True:
                current_angle = adaptateur.getAngleParcouru()
                angle_parcouru = abs(current_angle - start_angle)
                if angle_parcouru >= abs(angle):
                    adaptateur.setVitAngGA(0)
                    adaptateur.setVitAngDA(0)
                    break
                print(f"Je suis en train de tourner... ({angle_parcouru:.2f}/{abs(angle)}°)")
                sleep(0.5)
            elapsed_time = time() - start_time
            print(f"J'ai tourné à {direction} de {abs(angle)}° en {elapsed_time:.2f} secondes")
            sleep(0.5)
            print(f"Angle total parcouru : {abs(angle):.2f}°")
            adaptateur.arreter()
            print("J’ai fini de tourner !")
        return True

    else:
        print("Choix invalide.")
        return False

def relancer_strategie(controleur, adaptateur, action, type_simulation="simule"):
    """
    Relance une stratégie en fonction de l'action reçue (touches ou input).
    """
    if action == "tracer_carre":
        longueur_cote = float(input("Entrez la longueur du côté du carré (cm) : "))
        strat_carre = setStrategieCarre(longueur_cote)
        controleur.lancerStrategie(strat_carre)
        print("Stratégie 'tracer_carre' relancée.")
        return True
    elif action == "automatique":
        try:
            vitAngG = float(input("Entrez la vitesse angulaire de la roue gauche (vitAngG) : "))
            vitAngD = float(input("Entrez la vitesse angulaire de la roue droite (vitAngD) : "))
            strat_auto = StrategieAuto(vitAngG, vitAngD)
            controleur.lancerStrategie(strat_auto)
            print("Stratégie 'automatique' relancée.")
            return True
        except ValueError:
            print("Erreur : Valeurs invalides.")
            return False
    elif action == "suivre_balise":
        balise_x = float(input("Entrez la coordonnée x de la balise (cm) : "))
        balise_y = float(input("Entrez la coordonnée y de la balise (cm) : "))
        strat_balise = StrategieSuivreBalise((balise_x, balise_y))
        controleur.lancerStrategie(strat_balise)
        print("Stratégie 'suivre balise' relancée.")
        return True
    return False
