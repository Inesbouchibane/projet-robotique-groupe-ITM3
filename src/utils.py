# src/utils.py
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
VIT_ANG_AVAN_MUR = 1.5   # ou 2.0

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

def get_limits(color):
    if color == "red":
        return [(np.array([0, 100, 50]), np.array([20, 255, 255])),
                (np.array([160, 100, 50]), np.array([180, 255, 255]))]
    elif color == "blue":
        return [(np.array([100, 100, 50]), np.array([140, 255, 255]))]
    elif color == "green":
        return [(np.array([40, 100, 50]), np.array([80, 255, 255]))]
    elif color == "yellow":
        return [(np.array([20, 100, 50]), np.array([40, 255, 255]))]
    return []

def contientBalise(image):
    if image is None:
        return False, 0
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    center_x = image.shape[1] // 2
    decalage = 0
    detected = False

    for color in ["red", "blue", "green", "yellow"]:
        for lower, upper in get_limits(color):
            mask = cv2.inRange(hsv_image, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) > 500:
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        decalage += cx - center_x
                        detected = True

    return detected, decalage
