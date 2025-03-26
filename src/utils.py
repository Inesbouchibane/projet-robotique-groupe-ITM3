import math

def getAngleFromVect(v1, v2):
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    det = v1[0] * v2[1] - v1[1] * v2[0]
    return math.degrees(math.atan2(det, dot))

def getDistanceFromPts(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def normaliserVecteur(v):
    norm = math.sqrt(v[0]**2 + v[1]**2)
    return [v[0]/norm, v[1]/norm] if norm != 0 else v

# Constantes
VIT_ANG_AVAN, VIT_ANG_TOUR = 5, 3
TIC_CONTROLEUR = 0.01  # Mise à jour rapide
TIC_SIMULATION = 0.01  # Mise à jour rapide
LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1 = 800, 600, 10
LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE = 20, 40, 10, 5
LIST_PTS_OBS_RECTANGLE1 = [(100, 100), (150, 150), (200, 100)]
LIST_PTS_OBS_CARRE = [(300, 300), (350, 300), (350, 350), (300, 350)]
LIST_PTS_OBS_RECTANGLE3 = [(400, 400), (450, 450), (500, 400), (450, 350)]

