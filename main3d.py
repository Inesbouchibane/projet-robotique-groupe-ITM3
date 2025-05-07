# main3d.py
from src.robot.robot_simule import RobotSimule
from src.controleur.adapt_simule import AdaptateurSimule
from src.controleur.controleur import Controler
from src.environnement import Environnement
from src.interface_graphique.interface3D.interface3d import Affichage3D
from src.utils import LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1, LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_TRIANGLE, LIST_PTS_OBS_CERCLE
import logging
from src.interface_graphique.interface3D.menu3d import gerer_touches, afficher_instructions  # Importer les fonctions

logging.basicConfig(level=logging.DEBUG)

# Initialisation
envi = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
robot_sim = RobotSimule("r1", 500, 250, 25, 30, 50, 5, "lightblue")
adaptateur = AdaptateurSimule(robot_sim, envi)
envi.setRobot(adaptateur)

# Ajout des obstacles
for n, pts in [('Rectangle', LIST_PTS_OBS_RECTANGLE1), ('Triangle', LIST_PTS_OBS_TRIANGLE), ('Cercle', LIST_PTS_OBS_CERCLE)]:
    envi.addObstacle(n, pts)

# Initialisation du contrôleur
controleur = Controler(adaptateur)

# Initialisation de l'interface 3D avec Panda3D
affichage3d = Affichage3D(LARGEUR_ENV, LONGUEUR_ENV, [o.points for o in envi.listeObs])
affichage3d.robot = robot_sim  # Lier le robot simulé
affichage3d.adaptateur = adaptateur  # Lier l'adaptateur
affichage3d.controleur = controleur  # Lier le contrôleur pour les stratégies
affichage3d.envi = envi  # Lier l'environnement pour refreshEnvironnement

# Configurer la gestion des touches
afficher_instructions()  # Afficher les instructions au démarrage
gerer_touches(affichage3d)  # Configurer les touches

# Lancer l'application Panda3D
affichage3d.run()
