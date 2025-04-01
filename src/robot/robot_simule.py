    def avancer(self, valeur):
        vitesse_angulaire = valeur / (self.taille_roue / 2)  # Correction : rayon, pas diamètre
        self.vitAngG = vitesse_angulaire
        self.vitAngD = vitesse_angulaire
