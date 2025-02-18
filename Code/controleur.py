import logging
from environnement import Environnement

class Controleur:
    def __init__(self, vitesse_gauche, vitesse_droite, mode ,affichage=True, longueur_carre=200):
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
         """ Test du démarrage de la simulation """
        self.controleur.demarrer_simulation()
        # Vérifie que la méthode demarrer_simulation a bien été appelée sur l'objet env_mock
        self.env_mock.demarrer_simulation.assert_called_once() 

    
    def ajuster_vitesse(self, vitesse_gauche, vitesse_droite):
        """
        Permet d'ajuster les vitesses du robot en cours de simulation.
        """
        self.env.robot.vitesse_gauche = vitesse_gauche
        self.env.robot.vitesse_droite = vitesse_droite
        self.logger.info("Vitesses ajustées: vg=%.2f, vd=%.2f", vitesse_gauche, vitesse_droite)



