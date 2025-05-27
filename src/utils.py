import math
import cv2
import numpy as np

TIC_SIMULATION = 0.02
TIC_CONTROLEUR = 0.02
LARGEUR_ENV = 1000
LONGUEUR_ENV = 500
SCALE_ENV_1 = 1
VIT_ANG_AVAN = 2  # Slower speed for visible movement (units/sec)
VIT_ANG_TOUR = 1  # Angular speed for turns (radians/sec)

# Obstacle 1 : Rectangle
LIST_PTS_OBS_RECTANGLE1 = [(100, 100), (200, 100), (200, 150), (100, 150)]

# Obstacle 2 : Triangle
LIST_PTS_OBS_TRIANGLE = [(300, 200), (350, 250), (325, 175)]

# Obstacle 3 : Cercle (approximation avec 8 points)
def generate_circle_points(center_x, center_y, radius, num_points=8):
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    return points

LIST_PTS_OBS_CERCLE = generate_circle_points(650, 325, 50)

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

def contientBalise(image):
    """ Détermine si une image contient la balise
        :param image: l'image où on souhaite détecter la balise
        :returns: True si la balise se trouve dans l'image, False sinon
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    x, y = 0, 0
    colors_detected = 0

    for color in ["red", "blue", "green", "yellow"]:
        scope = get_limits(color)
        mask = cv2.inRange(hsv, scope[0], scope[1])
        moments = cv2.moments(mask)
        if moments["m00"] != 0:
            cX = int(moments["m10"] / moments["m00"])
            cY = int(moments["m01"] / moments["m00"])
            x += cX
            y += cY
            colors_detected += 1
        else:
            return (False, 0)

    if colors_detected < 4:
        return (False, 0)

    x = int(x / 4)
    y = int(y / 4)
    return (True, (x - (image.shape[1] / 2)))

def get_limits(color):
    """ Donne les nuances max et min de la couleur en paramètre """
    if color == "blue": 
        lower_limit = np.array([90, 70, 50])
        upper_limit = np.array([130, 255, 255])
    elif color == "red":
        lower_limit = np.array([0, 120, 70])
        upper_limit = np.array([20, 255, 255])
    elif color == "green":
        lower_limit = np.array([40, 50, 50])
        upper_limit = np.array([80, 255, 255])
    elif color == "yellow":
        lower_limit = np.array([20, 100, 100])
        upper_limit = np.array([40, 255, 255])
    elif color == "white":
        lower_limit = np.array([0, 0, 200])
        upper_limit = np.array([180, 30, 255])

    return lower_limit, upper_limit