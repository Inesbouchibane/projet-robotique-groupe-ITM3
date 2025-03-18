from threading import Thread
from time import sleep
from robot.robot import Robot
from robot.adapt import Adaptateur_simule
from environnement import Environnement
from affichage import Affichage
from controleur.controleur import Controler
from controleur.strategies import setStrategieCarre, StrategieAuto  
from utils import TIC_SIMULATION, LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1, 
LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_CARRE, LIST_PTS_OBS_RECTANGLE3
from logging import basicConfig, INFO

basicConfig(level=INFO)

envi = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
robot1 = Robot("r1", 500, 250, 20, 40, 10, 5, "lightblue")
adaptateur = Adaptateur_simule(robot1, envi)
envi.setRobot(adaptateur)

for n, pts in [('R1', LIST_PTS_OBS_RECTANGLE1), ('R2', LIST_PTS_OBS_CARRE), ('R3', LIST_PTS_OBS_RECTANGLE3)]:
     envi.addObstacle(n, pts)

affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, [o.get_bounding_box() for o in envi.listeObs])
