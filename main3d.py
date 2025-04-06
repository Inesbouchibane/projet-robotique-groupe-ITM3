# main3d.py

from src.robot.robot_simule import RobotSimule
from src.controleur.adapt_simule import AdaptateurSimule
from src.controleur.controleur import Controler
from src.environnement import Environnement
from src.interface_graphique.interface3D.interface3d import Affichage3D
from src.interface_graphique.interface3D.menu3d import gerer_evenements, afficher_instructions
from src.utils import LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1, LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_TRIANGLE, LIST_PTS_OBS_CERCLE
import logging
import math

logging.basicConfig(level=logging.DEBUG)  # Pour voir les logs

# Initialisation
envi = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
robot_sim = RobotSimule("r1", 500, 250, 25, 30, 50, 5, "lightblue")  # Orientation à 180° (dos visible)
adaptateur = AdaptateurSimule(robot_sim, envi)
envi.setRobot(adaptateur)

# Ajout des obstacles
for n, pts in [('Rectangle', LIST_PTS_OBS_RECTANGLE1), ('Triangle', LIST_PTS_OBS_TRIANGLE), ('Cercle', LIST_PTS_OBS_CERCLE)]:
    envi.addObstacle(n, pts)

# Initialisation du contrôleur
controleur = Controler(adaptateur)

# Initialisation de l'interface 3D
affichage3d = Affichage3D(LARGEUR_ENV, LONGUEUR_ENV, [o.points for o in envi.listeObs])

# Afficher les instructions
afficher_instructions()

# Boucle principale
running = True
while running:
    envi.refreshEnvironnement()  # Met à jour la position du robot et vérifie les collisions
    action = gerer_evenements(controleur)  # Gestion des stratégies
    if action == "quit":
        running = False
    
    # Calcul de l'orientation en degrés à partir de direction (cos_a, sin_a)
    orientation = math.degrees(math.atan2(robot_sim.direction[1], robot_sim.direction[0]))
    print(f"Position robot : ({robot_sim.x:.2f}, {robot_sim.y:.2f}), Orientation : {orientation:.2f}°")  # Débogage
    affichage3d.mettre_a_jour(robot_sim)  # Gère le rendu et la caméra

affichage3d.attendre_fermeture()