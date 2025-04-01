    def avancer(self, valeur):
        vitesse_angulaire = valeur / (self.taille_roue / 2)  # Correction : rayon, pas diamètre
        self.vitAngG = vitesse_angulaire
        self.vitAngD = vitesse_angulaire
        
        
    
    
    
    
    def getDistanceParcouru(self):
        return self.distance_parcourue

    def getDistanceObstacle(self):
        return float('inf')
