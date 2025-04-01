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
