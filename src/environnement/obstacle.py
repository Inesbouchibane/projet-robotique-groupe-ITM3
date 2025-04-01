import math

class Obstacle:
    def __init__(self, nom, points):
        self.nom = nom
        self.points = points

    def get_bounding_box(self):
        if not self.points:
            return None
        min_x = min(p[0] for p in self.points)
        max_x = max(p[0] for p in self.points)
        min_y = min(p[1] for p in self.points)
        max_y = max(p[1] for p in self.points)
        return (min_x, min_y, max_x - min_x, max_y - min_y)
