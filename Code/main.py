from controleur import Controleur

def main():
    try:
        vitesse_gauche = float(input("Entrez la vitesse de la roue gauche : "))
        vitesse_droite = float(input("Entrez la vitesse de la roue droite : "))
    except ValueError:
        print("Veuillez entrer des nombres pour les vitesses.")
        return

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
