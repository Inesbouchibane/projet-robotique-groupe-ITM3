import pygame
from src import (
    StrategieAvancer, StrategieAuto
)
from logging import getLogger

logger = getLogger(__name__)

def gerer_evenements(controleur):
    logger.debug("Début de gerer_evenements")
    events = pygame.event.get()
    if not events:
        logger.debug("Aucun événement détecté dans cette frame")
    for event in events:
        logger.info(f"Événement capturé : type={event.type}")
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
            elif event.key == pygame.K_m:
                logger.info("!!! TOUCHE 'm' PRESSÉE - LANCEMENT STRATEGIE ARRET MUR !!!")
                controleur.set_strategie("arret_mur", distarret=50)
                controleur.lancerStrategie()
                logger.info("Stratégie 'arret_mur' lancée")
            else:
                logger.info(f"Touche non gérée : {key_name}")
    logger.debug("Fin de gerer_evenements")
    return None

def afficher_instructions():
    print("Commandes disponibles dans la fenêtre :")
    print("- 'c' : Tracer un carré (100 unités)")
    print("- 'a' : Avancer (100 unités)")
    print("- 'r' : Mode automatique (vitesses 14, 7)")
    print("- 'm' : S'arrêter à 50 unités d'un mur/obstacle")
    print("- 'ESC' : Quitter")