import logging
from environnement import Environnement

class Controleur:
    def __init__(self, vitesse_gauche, vitesse_droite, mode):
	"""
        Initialise le contrôleur avec les paramètres de simulation.
        :param vitesse_gauche: Vitesse de la roue gauche.
        :param vitesse_droite: Vitesse de la roue droite.
        :param mode: "automatique", "manuel" ou "carré".
        :param affichage: True pour affichage graphique, False pour console.
        :param longueur_carre: Longueur du côté du carré (pour le mode carré).
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.env = Environnement(vitesse_gauche, vitesse_droite, mode, affichage, longueur_carre)
        self.logger.info("Contrôleur initialisé en mode: %s", mode)

    def demarrer_simulation(self):
        """
        Démarre la simulation en fonction du mode choisi.
        """
        self.env.boucle_principale()
    
    def ajuster_vitesse(self, vitesse_gauche, vitesse_droite):
        """
        Ajuste les vitesses des roues du robot.
        :param vitesse_gauche: Nouvelle vitesse de la roue gauche.
        :param vitesse_droite: Nouvelle vitesse de la roue droite.
        """
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite
        self.env.robot.vitesse_gauche = vitesse_gauche
        self.env.robot.vitesse_droite = vitesse_droite

