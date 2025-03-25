from robot import Robot

class RobotReel(Robot):
    """Classe représentant un robot réel."""

    def __init__(self, nom, x, y, width, length, height, rayonRoue, couleur):
        """Initialise le robot réel avec ses caractéristiques physiques."""
        super().__init__(nom, x, y, width, length, height, rayonRoue, couleur)
        self.capteur_distance = None  # Capteur de distance (à définir)
