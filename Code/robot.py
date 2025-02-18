import math

class Robot:
    def __init__(self, x, y, vitesse_gauche, vitesse_droite):
        """
        Initialise l'affichage graphique.
        :param largeur: Largeur de la fenêtre.
        :param hauteur: Hauteur de la fenêtre.
        :param obstacles: Liste des obstacles à dessiner.
        """
        self.x, self.y = x, y
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite
        self.angle = 0
        self.largeur, self.longueur = 20, 40
        

    def deplacer(self):
        vitesse_moyenne = (self.vitesse_gauche + self.vitesse_droite) / 2
        delta_angle = (self.vitesse_droite - self.vitesse_gauche) / self.largeur * 10
        self.angle = (self.angle + delta_angle) % 360
        dx = vitesse_moyenne * math.cos(math.radians(self.angle))
        dy = -vitesse_moyenne * math.sin(math.radians(self.angle))
        nouvelle_x = self.x + dx
        nouvelle_y = self.y + dy
        # S'assurer que le robot reste dans la fenêtre (0,800)x(0,600)
        if 0 < nouvelle_x < 800 and 0 < nouvelle_y < 600:
            self.x = nouvelle_x
            self.y = nouvelle_y
            
        
    
    def scan_infrarouge(self, obstacles, max_distance):
        angle_rad = math.radians(self.angle)
        for d in range(0, int(max_distance), 5):
            x_point, y_point = self.x + d * math.cos(angle_rad), self.y - d * math.sin(angle_rad)
            for ox, oy, ow, oh in obstacles:
                if ox < x_point < ox + ow and oy < y_point < oy + oh:
                    return (x_point, y_point)
        return (self.x + max_distance * math.cos(angle_rad), self.y - max_distance * math.sin(angle_rad))
