import math

TIC_SIMULATION = 0.02
TIC_CONTROLEUR = 0.02
LARGEUR_ENV = 1000
LONGUEUR_ENV = 500
SCALE_ENV_1 = 1
VIT_ANG_AVAN = 2  # Slower speed for visible movement (units/sec)
VIT_ANG_TOUR = 1  # Angular speed for turns (radians/sec)

# Obstacle 1 : Rectangle
LIST_PTS_OBS_RECTANGLE1 = [(450, 375), (550, 375), (550, 425), (450, 425)]

#Obstacle2 : Triangle : on le met au milieu 
LIST_PTS_OBS_TRIANGLE = [(475, 225), (525, 275), (500, 250)]

 
def generate_circle_points(center_x, center_y, radius, num_points=8):
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    return points

#Obstacle 3 : Cercle -> modification que des valeurs pas de la forme des 
obstacles
LIST_PTS_OBS_CERCLE = generate_circle_points(500, 100, 30)

def getDistanceFromPts(pt1, pt2):
    return math.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)

def normaliserVecteur(vecteur):
    norme = math.sqrt(vecteur[0]**2 + vecteur[1]**2)
    if norme == 0:
        return [0, 0]
    return [vecteur[0] / norme, vecteur[1] / norme]

def normalize_angle(angle):
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle
