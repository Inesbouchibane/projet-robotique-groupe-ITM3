
from src.robot.robot_simule import RobotSimule
from src.controleur.adapt_simule import AdaptateurSimule
from src.controleur.controleur import Controler
from src.environnement.environnement import Environnement
from src.interface_graphique.interface2D.interface2d import Affichage
from src.utils import LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1, TIC_SIMULATION
from time import sleep

### Q 1.1 ###
def q1_1():
    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    env.addObstacle("cercle", [(LARGEUR_ENV // 2, LONGUEUR_ENV // 2)])  
    env.addObstacle("rectangle", [(LARGEUR_ENV // 2, 50)])               
    env.addObstacle("triangle", [(LARGEUR_ENV // 2, LONGUEUR_ENV - 50)])
    robot = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)
    adaptateur = AdaptateurSimule(robot, env)
    env.setRobot(adaptateur)
    controler = Controler(adaptateur)
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, env.listePointsObstacles)
    affichage.loop(env, adaptateur, controler)

### Q 1.2 ###
class StrategieDemiTour:
    def __init__(self):
        self.compteur = 0

    def start(self, adaptateur):
        self.compteur = 0
        adaptateur.setVitAngA(30)

    def step(self, adaptateur):
        if self.compteur >= 10:
            adaptateur.seArreter()
            return
        if adaptateur.getDistanceObstacle() < 40:
            adaptateur.setVitAngG(-30)
            adaptateur.setVitAngD(30)
            sleep(1)
            self.compteur += 1
            adaptateur.setVitAngA(30)

    def stop(self, adaptateur):
        adaptateur.seArreter()

def q1_2():
    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    robot = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)
    adaptateur = AdaptateurSimule(robot, env)
    env.setRobot(adaptateur)
    strat = StrategieDemiTour()
    strat.start(adaptateur)
    while strat.compteur < 10:
        strat.step(adaptateur)
        env.refreshEnvironnement()
        sleep(TIC_SIMULATION)
    strat.stop(adaptateur)

### Q 1.3 ###
def q1_3():
    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    robot = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)
    adaptateur = AdaptateurSimule(robot, env)
    env.setRobot(adaptateur)
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, env.listePointsObstacles)
    affichage.dessine(True)  # Lancer le dessin
    affichage.ajouterRobot(robot)
    affichage.afficher(env)

### Q 1.4 ###
def q1_4():
    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    robot = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)
    adaptateur = AdaptateurSimule(robot, env)
    env.setRobot(adaptateur)
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, env.listePointsObstacles)
    affichage.bleu()  # Passer à la couleur bleue
    affichage.dessine(True)
    affichage.afficher(env)

### Q 1.5 ###
def q1_5():
    # Stratégie pour faire dessiner en bleu
    def StrategieBleu():
        affichage.bleu()
        affichage.dessine(True)
    
    # Stratégie pour faire dessiner en rouge
    def StrategieRouge():
        affichage.rouge()
        affichage.dessine(True)
    
    # Stratégie pour ne pas dessiner
    def StrategieInvisible():
        affichage.dessine(False)
    
    # Utilisation des stratégies combinées
    robot = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)
    adaptateur = AdaptateurSimule(robot, env)
    env.setRobot(adaptateur)

    StrategieRouge()
    q1_2()  # Appliquer la stratégie avec la fonction de mouvement

    StrategieBleu()
    q1_2()  # Appliquer la stratégie avec la fonction de mouvement

### Q 2.1 ###
def q2_1():
    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    robot1 = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)
    robot2 = RobotSimule("chat", 100, 0, 25, 30, 5, 20)
    adaptateur1 = AdaptateurSimule(robot1, env)
    adaptateur2 = AdaptateurSimule(robot2, env)
    env.setRobot(adaptateur1)
    env.setRobot(adaptateur2)
    controler1 = Controler(adaptateur1)
    controler2 = Controler(adaptateur2)
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, env.listePointsObstacles)
    affichage.loop(env, adaptateur1, controler1)

### Q 2.2 ###
def q2_2():
    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    robot1 = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)
    robot2 = RobotSimule("chat", 100, 0, 25, 30, 5, 20)
    adaptateur1 = AdaptateurSimule(robot1, env)
    adaptateur2 = AdaptateurSimule(robot2, env)
    env.setRobot(adaptateur1)
    env.setRobot(adaptateur2)
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, env.listePointsObstacles)
    affichage.dessine(True)
    affichage.afficher(env)

### Q 2.3 ###
def q2_3():
    robot1 = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)
    robot2 = RobotSimule("chat", 100, 0, 25, 30, 5, 20)
    adaptateur1 = AdaptateurSimule(robot1, env)
    adaptateur2 = AdaptateurSimule(robot2, env)
    env.setRobot(adaptateur1)
    env.setRobot(adaptateur2)
    distance = getDistanceFromPts(robot1.x, robot1.y, robot2.x, robot2.y)
    if distance < 2 * robot1.diametre:
        print("Le chat attrape la souris.")
    else:
        print("Le chat ne peut pas attraper la souris.")
