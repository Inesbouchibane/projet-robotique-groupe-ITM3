# tmesolo.py


from src.robot.robot_simule import RobotSimule
from src.controleur.adapt_simule import AdaptateurSimule
from src.controleur.controleur import Controler
from src.environnement.environnement import Environnement
from src.interface_graphique.interface2D.interface2d import Affichage
from src.utils import LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1, TIC_SIMULATION
from time import sleep

### Q 1.1 ###
def q1_1():
    # Création de l'envirronement avec des obstacles 
    # Ces obstacles sont placé au centre et aux positions haut et bas du milieu de l'arène.
    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    env.addObstacle("cercle", [(LARGEUR_ENV // 2, LONGUEUR_ENV // 2)])  # centre
    env.addObstacle("rectangle", [(LARGEUR_ENV // 2, 50)])               # haut milieu
    env.addObstacle("triangle", [(LARGEUR_ENV // 2, LONGUEUR_ENV - 50)])# bas milieu
    robot = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)  # Creation du robot 'souris'
    adaptateur = AdaptateurSimule(robot, env)
    env.setRobot(adaptateur)
    controler = Controler(adaptateur)
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, env.listePointsObstacles)
    affichage.loop(env, adaptateur, controler)

### Q 1.2 ###
# Création de la stratégie de demi-tour qui fait avancer le robot et le fait tourner 
# lorsqu'il détecte un obstacle à moins de 40 unités
class StrategieDemiTour:
    def __init__(self):
        self.compteur = 0  # on initialise le compteur de demi-tours

    def start(self, adaptateur):
        self.compteur = 0  # remettre le compteur à zéro
        adaptateur.setVitAngA(30)  # on avance avec une vitesse angulaire positive

    def step(self, adaptateur):
        if self.compteur >= 10:  # si on a fait 10 demi-tours, on arrête
            adaptateur.seArreter()
            return
        if adaptateur.getDistanceObstacle() < 40:  # Si trop près d'un obstacle, faire un demi-tour
            adaptateur.setVitAngG(-30)
            adaptateur.setVitAngD(30)
            sleep(1)  # temps de rotation
            self.compteur += 1  # incrémente le compteur de demi-tours
            adaptateur.setVitAngA(30)  # reprendre la vitesse d'avancée

    def stop(self, adaptateur):
        adaptateur.seArreter()  # stop du robot une fois les 10 demi-tours faits

def q1_2():
    # Initialisation de l'envirronement et du robot 'souris'
    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    robot = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)
    adaptateur = AdaptateurSimule(robot, env)
    env.setRobot(adaptateur)
    strat = StrategieDemiTour()  # on choisit la stratégie de demi-tour
    strat.start(adaptateur)  # on démarre la stratégie
    while strat.compteur < 10:  # tant que le robot n'a pas fait 10 demi-tours
        strat.step(adaptateur)  # exécution d'un pas de la stratégie
        env.refreshEnvironnement()  # actualisation de l'environnement
        sleep(TIC_SIMULATION)  # pause entre chaque mise à jour
    strat.stop(adaptateur)  # on arrête le robot à la fin

### Q 1.3 ###
def q1_3():
    # Création de l'envirronement avec un robot 'souris' qui va dessiner sa trace
    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    robot = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)
    adaptateur = AdaptateurSimule(robot, env)
    env.setRobot(adaptateur)
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, env.listePointsObstacles)
    affichage.dessine(True)  # Activer le mode dessin
    affichage.ajouterRobot(robot)
    affichage.afficher(env)  # Afficher l'environnement avec la trace

### Q 1.4 ###
def q1_4():
    # Création de l'environnement avec un robot 'souris' et une trace rouge
    env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
    robot = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)
    adaptateur = AdaptateurSimule(robot, env)
    env.setRobot(adaptateur)
    affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, env.listePointsObstacles)
    affichage.rouge()  # changer la couleur de la trace en rouge
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
    # Création de deux robots, 'souris' et 'chat', avec contrôleur indépendant
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
    # Le robot 'souris' dessine un carré, le robot 'chat' fait un aller-retour vertical
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
    # Le chat attrape la souris si la distance est inférieure à deux fois le diamètre de la souris
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

### Q 2.4 ###
def q2_4():
    # Le chat voit la souris dans un angle compris entre -10° et 10° par rapport à son orientation
    robot1 = RobotSimule("souris", 50, LONGUEUR_ENV - 50, 25, 30, 5, 20)
    robot2 = RobotSimule("chat", 100, 0, 25, 30, 5, 20)
    adaptateur1 = AdaptateurSimule(robot1, env)
    adaptateur2 = AdaptateurSimule(robot2, env)
    env.setRobot(adaptateur1)
    env.setRobot(adaptateur2)
    angle_souris = robot2.angle - robot1.angle
    if -10 <= angle_souris <= 10:
        print("Le chat voit la souris.")
    else:
        print("Le chat ne voit pas la souris.")
        
        

