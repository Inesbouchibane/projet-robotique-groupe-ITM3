class Balise:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_direction(self, robot):
        if self.x < robot.x:
            return "gauche"
        elif self.x > robot.x:
            return "droite"
        return "devant"