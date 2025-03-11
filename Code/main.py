
from controleur import Controleur

def main():
    mode = ""
    while mode.lower() not in ["a", "m", "c", "mur"]:
        mode = input("Mode : automatique (a), manuel (m), carré (c) ou avancer vers mur (mur) ? ").strip().lower()

    mode_str = {"a": "automatique", "m": "manuel", "c": "carré", "mur": "mur"}[mode]

    if mode_str in ["automatique", "manuel"]:
        try:
            vitesse_gauche = float(input("Vitesse de la roue gauche : "))
            vitesse_droite = float(input("Vitesse de la roue droite : "))
        except ValueError:
            print("Erreur: Utilisation des vitesses par défaut (2).")
            vitesse_gauche, vitesse_droite = 2, 2
    elif mode_str == "carré":  # mode "carré"
        try:
            vitesse = float(input("Vitesse des roues (par défaut 2) : ") or 2)
            vitesse_gauche, vitesse_droite = vitesse, vitesse
        except ValueError:
            print("Erreur: Utilisation de la vitesse par défaut (2).")
            vitesse_gauche, vitesse_droite = 2, 2
    else:  # mode "mur"
        try:
            vitesse = float(input("Vitesse des roues (par défaut 2) : ") or 2)
            vitesse_gauche, vitesse_droite = vitesse, vitesse
        except ValueError:
            print("Erreur: Utilisation de la vitesse par défaut (2).")
            vitesse_gauche, vitesse_droite = 2, 2

    try:
        pos_x = float(input("Position x initiale (0-800) : "))
        pos_y = float(input("Position y initiale (0-600) : "))
        if not (0 <= pos_x <= 800 and 0 <= pos_y <= 600):
            raise ValueError("Position hors limites (0-800, 0-600).")
    except ValueError as e:
        print(f"Erreur: {e}. Utilisation des valeurs par défaut (400, 300).")
        pos_x, pos_y = 400, 300

    longueur_carre = 200
    if mode_str == "carré":
        try:
            longueur_carre = float(input("Longueur du côté du carré : "))
            if longueur_carre <= 0:
                raise ValueError("La longueur doit être positive.")
        except ValueError as e:
            print(f"Erreur: {e}. Utilisation de 200.")
            longueur_carre = 200

    affichage_input = input("Affichage graphique ? (true/false) : ").strip().lower()
    affichage = affichage_input in ['true', 't', '1', 'oui']

    controleur = Controleur(vitesse_gauche, vitesse_droite, mode_str, affichage, longueur_carre, pos_x, pos_y)

    if mode_str == "mur":
        controleur.avancer_vers_mur_proche()
    else:
        controleur.env.demarrer_simulation()

if __name__ == "__main__":
    main()
