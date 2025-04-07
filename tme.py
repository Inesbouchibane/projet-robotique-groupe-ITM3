# tme.py
import sys
from src.interface_graphique.interface2D.interface2d import Affichage as 
Affichage2D
from src.interface_graphique.interface3D.interface3d import Affichage3D
from src.utils import *
from src.environnement import Environnement
from src.robot.robot_simule import RobotSimule
from src.controleur.adapt_simule import AdaptateurSimule
from src.controleur.controleur import Controler
from src.interface_graphique.interface2D.menu2d import gerer_evenements as 
gerer_evenements_2d
from src.interface_graphique.interface3D.menu3d import gerer_evenements as 
gerer_evenements_3d, afficher_instructions as afficher_instructions_3d
from time import sleep
import logging




