class Balise:
    """Classe représentant une balise pour guider le robot."""

    def __init__(self, x, y):
        """Initialise la balise avec ses coordonnées."""
        self.x = x
        self.y = y

    def get_direction(self, robot):
        """Retourne la direction de la balise par rapport au robot."""
        if self.x < robot.x:
            return "gauche"
        elif self.x > robot.x:
            return "droite"
        return "devant"

