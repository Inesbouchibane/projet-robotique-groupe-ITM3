from controleur import Controleur

def main():
    try:
        vitesse_gauche = float(input("Entrez la vitesse de la roue gauche : "))
        vitesse_droite = float(input("Entrez la vitesse de la roue droite : "))
    except ValueError:
        print("Veuillez entrer des nombres pour les vitesses.")
        return

    
        try:
        pos_x = float(input("Position x initiale (0-800) : "))
        pos_y = float(input("Position y initiale (0-600) : "))
        if not (0 <= pos_x <= 800 and 0 <= pos_y <= 600):
            raise ValueError("Position hors limites (0-800, 0-600).")
    except ValueError as e:
        print(f"Erreur: {e}. Utilisation des valeurs par défaut (400, 300).")
        pos_x, pos_y = 400, 300


    mode = ""
    while mode.lower() not in ["a", "m", "c"]:
        mode = input("Choisissez le mode : automatique (a), manuel (m) ou carré (c) ? ")

    if mode.lower() == "a":
        mode_str = "automatique"
    elif mode.lower() == "m":
        mode_str = "manuel"
    else:
        mode_str = "carré"

    longueur_carre = 200  # Valeur par défaut
    if mode_str == "carré":
        try:
            longueur_carre = float(input("Entrez la longueur du côté du carré : "))
        except ValueError:
            print("Valeur invalide, utilisation de 200.")
            longueur_carre = 200

    affichage_input = input("Voulez-vous l'affichage graphique ? (true/false) : ").strip().lower()
    affichage = affichage_input in ['true', 't', '1', 'oui']

    controleur = Controleur(vitesse_gauche, vitesse_droite, mode_str, affichage, longueur_carre)
    controleur.demarrer_simulation()

if __name__ == "__main__":
    main()
