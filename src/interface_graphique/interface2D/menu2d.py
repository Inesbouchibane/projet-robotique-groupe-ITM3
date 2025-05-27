import pygame
from src.controleur.strategies import StrategieAvancer, setStrategieCarre, StrategieArretMur, StrategieSuivreBalise, StrategieClavier, StrategieTourner  # Add StrategieTourner
from logging import getLogger

logger = getLogger(__name__)

def afficher_instructions():
    print("=== Instructions 2D ===")
    print("Commandes disponibles :")
    print("  k - Contrôle par clavier (i pour avancer, o pour reculer, p pour gauche, l pour droite)")
    print("  a - Avancer de 100 mm")
    print("  c - Dessiner un carré de 100 mm par côté")
    print("  m - S'approcher à 5 mm d'un mur")
    print("  b - Suivre la balise avec la caméra")
    print("  t - Tourner d’un angle spécifié (en degrés)")  # New option
    print("  q - Quitter")
    print("===================")

def gerer_evenements(controleur, key_map):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            logger.info("Quit event received")
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                controleur.stop()
                controleur.set_strategie("avancer", distance=100)
                controleur.lancerStrategie()
                logger.debug("Stratégie 'avancer' lancée")
            elif event.key == pygame.K_c:
                controleur.stop()
                controleur.set_strategie("tracer_carre", longueur_cote=100)
                controleur.lancerStrategie()
                logger.debug("Stratégie 'tracer_carre' lancée")
            elif event.key == pygame.K_m:
                controleur.stop()
                controleur.set_strategie("arret_mur", adaptateur=controleur.adaptateur, distance_arret=5)
                controleur.lancerStrategie()
                logger.debug("Stratégie 'arret_mur' lancée")
            elif event.key == pygame.K_r:
                controleur.stop()
                controleur.set_strategie("auto", vitAngG=14, vitAngD=7)
                controleur.lancerStrategie()
                logger.debug("Stratégie 'auto' lancée")
            elif event.key == pygame.K_b:
                controleur.stop()
                controleur.set_strategie("suivre_balise", adaptateur=controleur.adaptateur)
                controleur.lancerStrategie()
                logger.debug("Stratégie 'suivre_balise' lancée")
            elif event.key == pygame.K_k:
                controleur.stop()
                key_map.update({'i': False, 'o': False, 'p': False, 'l': False})
                controleur.set_strategie("clavier", adaptateur=controleur.adaptateur, key_map=key_map)
                controleur.lancerStrategie()
                logger.debug("Stratégie 'clavier' lancée")
            elif event.key == pygame.K_t:
                try:
                    # Pygame doesn't support console input directly, so we'll log and assume a default angle or prompt via print
                    print("Entrez l’angle de rotation en degrés (positif pour gauche, négatif pour droite) : ")
                    angle = float(input())  # Note: This is not ideal in Pygame; consider a GUI input in a real application
                    if not -360 <= angle <= 360:
                        raise ValueError("L’angle doit être entre -360 et 360 degrés")
                    controleur.stop()
                    controleur.set_strategie(StrategieTourner, angle=angle)
                    controleur.lancerStrategie()
                    logger.debug(f"Stratégie 'tourner' lancée avec angle={angle}")
                except ValueError as e:
                    logger.error(f"Erreur lors de la saisie de l’angle : {e}")
                    print(f"Erreur : {e}")
            elif event.key == pygame.K_q:
                controleur.stop()
                logger.info("Arrêt demandé via 'q'")
                return "quit"
            elif event.key == pygame.K_i:
                key_map['i'] = True
                logger.debug("Key 'i' pressed")
            elif event.key == pygame.K_o:
                key_map['o'] = True
                logger.debug("Key 'o' pressed")
            elif event.key == pygame.K_p:
                key_map['p'] = True
                logger.debug("Key 'p' pressed")
            elif event.key == pygame.K_l:
                key_map['l'] = True
                logger.debug("Key 'l' pressed")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_i:
                key_map['i'] = False
                logger.debug("Key 'i' released")
            elif event.key == pygame.K_o:
                key_map['o'] = False
                logger.debug("Key 'o' released")
            elif event.key == pygame.K_p:
                key_map['p'] = False
                logger.debug("Key 'p' released")
            elif event.key == pygame.K_l:
                key_map['l'] = False
                logger.debug("Key 'l' released")

    if isinstance(controleur.strategie, StrategieClavier):
        controleur.strategie.key_map = key_map
        controleur.strategie.step(controleur.adaptateur)
        logger.debug(f"StrategieClavier updated with key_map: {key_map}")

    return None