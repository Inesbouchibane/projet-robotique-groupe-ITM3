    def avancer(self, valeur):
        vitesse_angulaire = valeur / (self.taille_roue / 2)  # Correction : rayon, pas diamètre
        self.vitAngG = vitesse_angulaire
        self.vitAngD = vitesse_angulaire
        
        
    
    
    
    
    def getDistanceParcouru(self):
        return self.distance_parcourue

    def getDistanceObstacle(self):
        return float('inf')
        
    def get_VitG(self):
        return self.vitAngG

    def get_VitD(self):
        return self.vitAngD
        
  def refresh(self, delta_t=None):
        if delta_t is None:
            current_time = time()
            delta_t = current_time - self.last_update
            self.last_update = current_time
        delta_t = max(delta_t, 0.02)  # Garantir un delta_t minimum (TIC_SIMULATION)

        if self.estCrash:
            self.arreter()
            return

        rayon_roue = self.taille_roue / 2
        v_gauche = self.vitAngG * rayon_roue
        v_droite = self.vitAngD * rayon_roue
        v = (v_gauche + v_droite) / 2
        omega = (v_droite - v_gauche) / self.width
