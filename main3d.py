from src.robot.robot_simule import RobotSimule
from src.controleur.adapt_simule import AdaptateurSimule
from src.controleur.controleur import Controler
from src.controleur.strategies import StrategieClavier
from src.environnement import Environnement
from src.interface_graphique.interface3D.interface3d import Affichage3D
from src.utils import LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1, LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_TRIANGLE, LIST_PTS_OBS_CERCLE
import logging
from src.interface_graphique.interface3D.menu3d import gerer_touches, afficher_instructions
from direct.task import Task
from time import sleep

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
# Set default strategy to StrategieClavier
key_map = {'i': False, 'o': False, 'p': False, 'l': False}
controleur.set_strategie("clavier", adaptateur=adaptateur, key_map=key_map)
controleur.lancerStrategie()
logger.debug("Contrôleur initialisé avec StrategieClavier par défaut")

# Initialisation de l'interface 3D avec Panda3D
affichage3d = Affichage3D(LARGEUR_ENV, LONGUEUR_ENV, [o.points for o in envi.listeObs])
affichage3d.robot = robot_sim
affichage3d.adaptateur = adaptateur
affichage3d.controleur = controleur
affichage3d.envi = envi
logger.debug("Interface 3D initialisée")

# Configurer la gestion des touches
afficher_instructions()
gerer_touches(affichage3d)

# Task to update environment and robot
def update_task(task):
    envi.refreshEnvironnement()
    affichage3d.mettre_a_jour(robot_sim)
    logger.debug("update_task: environnement et robot mis à jour")
    return Task.cont

affichage3d.taskMgr.add(update_task, "update_environment")

# Lancer l'application Panda3D
logger.debug("Lancement de l'application Panda3D")
affichage3d.run()