from robot import Robot

class RobotReel(Robot):
    """Classe représentant un robot réel."""

    def __init__(self, nom, x, y, width, length, height, rayonRoue, couleur):
        """Initialise le robot réel avec ses caractéristiques physiques."""
        super().__init__(nom, x, y, width, length, height, rayonRoue, couleur)
        self.capteur_distance = None  # Capteur de distance (à définir)


    def setMoteurDPS(self, vitesse_gauche, vitesse_droite):
        """Définit la vitesse en degré par seconde des moteurs gauche et droit."""
        self.vitAngG = vitesse_gauche
        self.vitAngD = vitesse_droite


    def getDistance(self):
        """Retourne la distance mesurée par le capteur (simulation du capteur réel)."""
        if self.capteur_distance:
            return self.capteur_distance.mesurer_distance()
        return float('inf')  # Valeur par défaut si aucun capteur n'est présent


