# src/interface_graphique/interface3D/menu3d.py

import pygame
from src import (
    StrategieAvancer, StrategieAuto, setStrategieCarre
)
from logging import getLogger

logger = getLogger(__name__)

def gerer_evenements(controleur):
    logger.debug("Début de gerer_evenements 3D")
    for event in [pygame.event.peek()]:
        if event.type == pygame.QUIT:
            logger.info("Événement QUIT détecté")
            return "quit"
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            logger.info(f"Touche pressée : {key_name}")
            if event.key == pygame.K_ESCAPE:
                logger.info("Touche ESC détectée")
                return "quit"
            elif event.key == pygame.K_c:
                controleur.set_strategie("tracer_carre", longueur_cote=100)
                controleur.lancerStrategie()
                logger.info("Stratégie 'tracer_carre' lancée")
            elif event.key == pygame.K_a:
                controleur.set_strategie("avancer", distance=100)
                controleur.lancerStrategie()
                logger.info("Stratégie 'avancer' lancée")
            elif event.key == pygame.K_r:
                controleur.set_strategie("auto", vitAngG=14, vitAngD=7)
                controleur.lancerStrategie()
                logger.info("Stratégie 'auto' lancée")
            else:
                logger.info(f"Touche non gérée : {key_name}")
    logger.debug("Fin de gerer_evenements 3D")
    return None

def afficher_instructions():
    print("Commandes disponibles dans la fenêtre 3D :")
    print("- 'c' : Tracer un carré (100 unités)")
    print("- 'a' : Avancer (100 unités)")
    print("- 'r' : Mode automatique (vitesses 14, 7)")
    print("- 'ESC' : Quitter")
    print("- 'UP' : Zoom avant (haut → rapprochée → vue du robot)")
    print("- 'DOWN' : Zoom arrière (robot → rapprochée → haut)")
    print("- 'LEFT' : Vue à gauche du robot")
    print("- 'RIGHT' : Vue à droite du robot")