import pygame
from environnement.environnement import Environnement
from robot.robot import Robot
from adapt.adapt_simule import Adaptateur_simule
from interface_graphique.affichage import Affichage
from robot.robot_mockup import RobotMockup
from utils import LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1, 
LIST_PTS_OBS_RECTANGLE1, LIST_PTS_OBS_CARRE, LIST_PTS_OBS_RECTANGLE3, VIT_ANG_AVAN, VIT_ANG_TOUR
from environnement.balise import Balise
from math import atan2, cos, sin, degrees

class Simulation2D:
    def __init__(self):
        print("Début de l'initialisation de Simulation2D")
        self.envi = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
        print("Environnement créé")
        self.robot = RobotMockup("SimuBot", 400, 300, 20, 40, 10, 5, "red")
        print("RobotMockup créé")
        self.adaptateur = Adaptateur_simule(self.robot, self.envi)
        print("Adaptateur créé")
        self.envi.setRobot(self.adaptateur)
        print("Robot ajouté à l'environnement")
        self.affichage = Affichage(LARGEUR_ENV, LONGUEUR_ENV, self._get_obstacles())
        print("Affichage initialisé")
        self.balise = Balise(600, 400)
        print("Balise créée")

    def _get_obstacles(self):
        print("Ajout des obstacles")
        obstacles = []
        for nom, points in [("R1", LIST_PTS_OBS_RECTANGLE1), ("R2", LIST_PTS_OBS_CARRE), ("R3", LIST_PTS_OBS_RECTANGLE3)]:
            self.envi.addObstacle(nom, points)
            obstacles.append(self.envi.listeObs[-1].get_bounding_box())
        print("Obstacles ajoutés")
        return obstacles

    
    def run(self):
        print("Début de la boucle run")
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    print("Événement QUIT détecté")

            dx = self.balise.x - self.robot.x
            dy = self.balise.y - self.robot.y
            angle_cible = atan2(dy, dx)
            angle_actuel = atan2(self.robot.direction[1], self.robot.direction[0])
            angle_diff = (angle_cible - angle_actuel + 3.14159) % (2 * 3.14159) - 3.14159

            if abs(angle_diff) > 0.1:
                if angle_diff > 0:
                    self.adaptateur.setVitAngGA(-VIT_ANG_TOUR / 2)
                    self.adaptateur.setVitAngDA(VIT_ANG_TOUR)
                    print(f"Tourne droite, angle_diff={degrees(angle_diff):.1f}°, vitG={self.robot.vitAngG}, vitD={self.robot.vitAngD}")
                else:
                    self.adaptateur.setVitAngGA(VIT_ANG_TOUR)
                    self.adaptateur.setVitAngDA(-VIT_ANG_TOUR / 2)
                    print(f"Tourne gauche, angle_diff={degrees(angle_diff):.1f}°, vitG={self.robot.vitAngG}, vitD={self.robot.vitAngD}")
            else:
                self.adaptateur.setVitAngA(VIT_ANG_AVAN)
                print(f"Avance, angle_diff={degrees(angle_diff):.1f}°, vitG={self.robot.vitAngG}, vitD={self.robot.vitAngD}")

            self.envi.refreshEnvironnement()
            print(f"Position après refresh: ({self.robot.x:.3f}, {self.robot.y:.3f})")
            self.affichage.mettre_a_jour(self.robot)
            clock.tick(30)

        print("Fin de la boucle run")
        pygame.quit()

if __name__ == "__main__":
    print("Lancement de la simulation")
    sim = Simulation2D()
    sim.run()

