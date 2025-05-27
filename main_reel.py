# main_reel.py
import logging
import time
import cv2  # Added for image saving
from src.robot.robot2IN013 import Robot2IN013
from src.controleur.adapt_reel import Adaptateur_reel
from src.controleur.controleur import Controler
from src.controleur.strategies import StrategieAvancer, setStrategieCarre, StrategieArretMur, StrategieSuivreBalise, StrategieTourner, StrategieAuto
from src.utils import contientBalise  # Added import
from time import sleep
import math
import curses

# Configuration des logs
logging.basicConfig(
    filename='logs.log',
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
    encoding='UTF-8'
)
logger = logging.getLogger(__name__)

def afficher_menu():
    """Affiche le menu des actions disponibles"""
    print("\n=== Menu Robot2IN013 ===")
    print("0 - Quitter")
    print("1 - Avancer de 100 mm")
    print("2 - Tracer un carré de 100 mm par côté")
    print("3 - Avancer et s'arrêter près d'un mur")
    print("4 - Suivre une balise")
    print("5 - Tourner d'un angle spécifié")
    print("6 - Tester la stratégie auto")
    print("k - Contrôle par clavier (flèches pour diriger, p pour arrêter)")
    print("t - Tester la caméra (capture et sauvegarde une image)")
    print("=======================")

def main():
    logger.info("Démarrage du programme main_reel.py")

    # Initialisation du robot
    try:
        robot = Robot2IN013()
        robot.start_recording()
        logger.info("Robot2IN013 initialisé")
        print(f"Camera status: {'Active' if robot.camera else 'Not initialized'}")
        print(f"Camera recording: {robot._recording}")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du robot : {e}")
        print(f"Erreur : Impossible d'initialiser le robot. Vérifiez la connexion. ({e})")
        return

    # Vérifier si la caméra est active
    if robot.camera is None or not robot._recording:
        logger.error("La caméra n'est pas initialisée ou ne capture pas")
        print("Erreur : La caméra n'est pas disponible. Vérifiez la connexion et l'activation (raspi-config).")
        robot.stop()
        return

    # Initialisation de l'adaptateur et du contrôleur
    try:
        adaptateur = Adaptateur_reel(robot)
        controleur = Controler(adaptateur)
        logger.info("Adaptateur et contrôleur initialisés")
    except Exception as e:
        logger.error(f"Erreur initialisation de l'adaptateur/contrôleur : {e}")
        print(f"Erreur : Impossible d'initialiser l'adaptateur/contrôleur. ({e})")
        robot.stop()
        robot.stop_recording()
        return

    running = True
    while running:
        afficher_menu()
        choix = input("Entrez votre choix (0-6, k, t) : ").strip()

        if choix == "0":
            logger.info("Arrêt du programme")
            print("Arrêt du robot et fermeture du programme...")
            controleur.stop()
            robot.stop()
            robot.stop_recording()
            running = False

        elif choix == "1":
            logger.info("Lancement de la stratégie Avancer (100 mm)")
            print("Avancer de 100 mm...")
            strategie = StrategieAvancer(100)
            adaptateur.initialise()
            controleur.lancerStrategie(strategie)
            while controleur.running:
                distance = adaptateur.getDistanceParcourue()
                print(f"Distance parcourue : {int(distance)} mm")
                sleep(0.01)
            print("Avancement terminé.")

        elif choix == "2":
            logger.info("Lancement de la stratégie Carré (100 mm)")
            print("Tracer un carré de 100 mm...")
            strategie = setStrategieCarre(100)
            adaptateur.initialise()
            controleur.lancerStrategie(strategie)
            while controleur.running:
                cur = strategie.liste_strategies[strategie.index] \
                    if strategie.index < len(strategie.liste_strategies) else None
                if isinstance(cur, StrategieAvancer):
                    d = adaptateur.getDistanceParcourue()
                    print(f"Côté {(strategie.index // 2) + 1} : {int(d)} mm parcourus")
                elif isinstance(cur, StrategieTourner):
                    a = adaptateur.getAngleParcouru()
                    print(f"Rotation {(strategie.index // 2) + 1} : {int(math.degrees(a))}°")
                sleep(0.02)
            print("Carré terminé.")

        elif choix == "3":
            # ─── 1) Test immédiat du capteur ─────────────────────────────
            print("\n2. Test capteur de distance...")
            try:
                distance_test = adaptateur.getDistanceA()
                if distance_test is None:
                    print("❌ Capteur de distance n’a rien renvoyé – retour au menu.")
                    continue
                print(f"✅ Capteur OK : distance mesurée = {int(distance_test)} mm")
            except Exception as e:
                print(f"❌ Erreur capteur : {e}")
                continue

            # ─── 2) Demande de la distance cible ─────────────────────────
            try:
                distance_arret = float(input("Distance d’arrêt (mm, 5–2000) : ").strip())
                if not 5 <= distance_arret <= 2000:
                    raise ValueError
            except ValueError:
                print("⚠️ Valeur invalide – retour au menu.")
                continue

            # ─── 3) Lancement de la Stratégie ArretMur ───────────────────
            logger.info(f"Lancement StrategieArretMur : {distance_arret} mm")
            print(f"\n➡️ Avance jusqu’à {distance_arret} mm du mur…")

            strategie = StrategieArretMur(adaptateur, distance_arret)
            adaptateur.initialise()
            controleur.lancerStrategie(strategie)

            # ─── 4) Affichage temps réel jusqu’à l’arrêt ─────────────────
            while controleur.running:
                dist = adaptateur.getDistanceA()
                if dist is not None:
                    print(f"📏 {int(dist)} mm ", end="\r", flush=True)
                sleep(0.08)

            print("\n✅ Robot arrêté à distance cible.")


        elif choix == "4":
            logger.info("Lancement de la stratégie SuivreBalise")
            print("Suivre la balise...")
            strategie = StrategieSuivreBalise(adaptateur)
            adaptateur.initialise()
            controleur.lancerStrategie(strategie)
            while controleur.running:
                try:
                    image = adaptateur.get_imageA()
                    if image is None:
                        print("Erreur : Aucune image de la caméra. Vérifiez la connexion.")
                        logger.error("Aucune image disponible pour la détection de balise")
                        controleur.stop()
                        adaptateur.arreter()
                        break
                    balise, decale = contientBalise(image)
                    distance = adaptateur.getDistanceA()
                    print(f"Balise: {balise}, Décalage: {decale}, Distance obstacle: {int(distance) if distance is not None else -1} mm")
                    if distance is not None and distance < 50:
                        print("ALERTE : Obstacle trop proche ! Arrêt.")
                        logger.warning("Obstacle détecté à moins de 50 mm")
                        controleur.stop()
                        adaptateur.arreter()
                        break
                except Exception as e:
                    logger.error(f"Erreur lors de la détection de balise : {e}")
                    print(f"Erreur balise : {e}")
                    controleur.stop()
                    adaptateur.arreter()
                    break
                sleep(0.1)
            print("Suivi de la balise terminé.")

        elif choix == "5":
            angle_input = input("Entrez l'angle de rotation en degrés (positif pour droite, négatif pour gauche) : ").strip()
            try:
                angle = float(angle_input)
                logger.info(f"Lancement de la stratégie Tourner ({angle} degrés)")
                print(f"Tourner de {angle} degrés...")
                strategie = StrategieTourner(angle)
                adaptateur.initialise()
                controleur.lancerStrategie(strategie)
                while controleur.running:
                    angle_parcouru = adaptateur.getAngleParcouru()
                    print(f"Angle parcouru : {int(math.degrees(angle_parcouru))} degrés")
                    sleep(0.01)
                print("Rotation terminée.")
            except ValueError:
                logger.error(f"Angle invalide : {angle_input}")
                print("Erreur : Veuillez entrer un angle valide (nombre).")

        elif choix == "6":
            try:
                vit_g = float(input("Vitesse angulaire gauche (dps) : ").strip())
                vit_d = float(input("Vitesse angulaire droite (dps) : ").strip())
                logger.info(f"Lancement de la stratégie Auto (vitG={vit_g}, vitD={vit_d})")
                print(f"Mode auto avec vitG={vit_g}, vitD={vit_d}...")
                strategie = StrategieAuto(vit_g, vit_d)
                adaptateur.initialise()
                controleur.lancerStrategie(strategie)
                while controleur.running:
                    sleep(0.1)
                print("Mode auto terminé.")
            except ValueError:
                logger.error(f"Vitesse invalide")
                print("Erreur : Veuillez entrer des vitesses valides (nombres).")

        elif choix == "k":
            logger.info("Lancement du mode contrôle par clavier (curses)")
            print("Contrôle manuel : flèches (haut/bas/gauche/droite) pour diriger, p pour arrêter")

            def display_message(stdscr, message, y=3):
                try:
                    stdscr.addstr(y, 0, message[:80])
                    stdscr.clrtoeol()
                    stdscr.refresh()
                except Exception as e:
                    logger.error(f"Erreur affichage curses : {e}")

            try:
                stdscr = curses.initscr()
                curses.noecho()
                curses.cbreak()
                stdscr.keypad(True)
                stdscr.nodelay(True)
                stdscr.timeout(10)  # Très rapide pour la réactivité
                stdscr.clear()
                stdscr.addstr(0, 0, "Contrôle du robot :\n")
                stdscr.addstr(1, 0, "Haut: Avancer | Bas: Reculer | Gauche: Tourner gauche | Droite: Tourner droite")
                stdscr.addstr(2, 0, "P: Retour menu")
                stdscr.refresh()
            except Exception as e:
                logger.error(f"Erreur initialisation curses : {e}")
                print(f"Erreur initialisation interface clavier : {e}")
                sleep(1)
                continue

            vit_base = 30.0  # Vitesse de base pour avancer/reculer
            vit_turn = 20.0  # Vitesse pour tourner
            vit_g = 0
            vit_d = 0
            try:
                while True:
                    try:
                        key = stdscr.getch()
                    except:
                        key = -1

                    vit_g = 0
                    vit_d = 0
                    action = "Aucune action"

                    if key != -1:
                        if key == curses.KEY_UP:
                            vit_g = vit_base
                            vit_d = vit_base
                            action = f"Avancer: vitG={vit_g:.1f}, vitD={vit_d:.1f}"
                        elif key == curses.KEY_DOWN:
                            vit_g = -vit_base
                            vit_d = -vit_base
                            action = f"Reculer: vitG={vit_g:.1f}, vitD={vit_d:.1f}"
                        elif key == curses.KEY_LEFT:
                            vit_g = -vit_turn
                            vit_d = vit_turn
                            action = f"Tourner gauche: vitG={vit_g:.1f}, vit_d={vit_d:.1f}"
                        elif key == curses.KEY_RIGHT:
                            vit_g = vit_turn
                            vit_d = -vit_turn
                            action = f"Tourner droite: vitG={vit_g:.1f}, vitD={vit_d:.1f}"
                        elif key == ord('p'):
                            adaptateur.arreter()
                            logger.info("Mode clavier arrêté par l'utilisateur")
                            display_message(stdscr, "Arrêté")
                            break
                        else:
                            action = f"Touche ignorée: {chr(key) if 32 <= key <= 126 else key}"

                        display_message(stdscr, action, y=4)

                    try:
                        adaptateur.tourne(vit_g, vit_d)
                        logger.debug(f"Commande moteurs: vitG={vit_g:.1f}, vitD={vit_d:.1f}")
                    except Exception as e:
                        logger.error(f"Erreur commande moteurs : {e}")
                        display_message(stdscr, f"Erreur moteurs: {e}", y=8)

                    try:
                        distance = adaptateur.getDistanceA()
                        if distance is not None:
                            logger.debug(f"Distance obstacle: {distance:.1f} mm")
                            display_message(stdscr, f"Distance obstacle: {int(distance)} mm", y=5)
                            if distance < 50:
                                adaptateur.arreter()
                                vit_g = 0
                                vit_d = 0
                                display_message(stdscr, f"ALERTE: Obstacle à {int(distance)} mm !", y=6)
                                logger.warning(f"Obstacle détecté à {distance:.1f} mm")
                        else:
                            display_message(stdscr, "Distance obstacle: Non disponible", y=5)
                    except Exception as e:
                        logger.error(f"Erreur capteur distance : {e}")
                        display_message(stdscr, f"Erreur capteur: {e}", y=6)

                    try:
                        image = adaptateur.get_imageA()
                        if image is None:
                            display_message(stdscr, "Aucune image disponible", y=7)
                            logger.error("Aucune image pour détection de balise en mode clavier")
                        else:
                            balise, decale = contientBalise(image)
                            logger.debug(f"Balise: {balise}, Décalage: {decale}")
                            display_message(stdscr, f"Balise: {'Détectée' if balise else 'Non détectée'}, Décalage: {decale}", y=7)
                    except Exception as e:
                        logger.error(f"Erreur détection balise : {e}")
                        display_message(stdscr, f"Erreur balise: {e}", y=7)

                    try:
                        if adaptateur.estCrash():
                            adaptateur.arreter()
                            vit_g = 0
                            vit_d = 0
                            display_message(stdscr, "ALERTE: Collision détectée !", y=8)
                            logger.warning("Collision détectée")
                    except Exception as e:
                        logger.error(f"Erreur détection collision : {e}")
                        display_message(stdscr, f"Erreur collision: {e}", y=8)

                    sleep(0.002)
            except Exception as e:
                logger.error(f"Erreur dans le mode clavier : {e}")
                print(f"Erreur mode clavier : {e}")
            finally:
                try:
                    adaptateur.arreter()
                    adaptateur.cleanup()
                    curses.endwin()
                except Exception as e:
                    logger.error(f"Erreur nettoyage curses : {e}")
                print("Mode clavier terminé, retour au menu.")

        elif choix == "t":
            logger.info("Test de la caméra")
            print("Capturing test image...")
            try:
                image = adaptateur.get_imageA()
                if image is None:
                    print("Erreur : Aucune image capturée. Vérifiez la caméra.")
                    logger.error("Échec de la capture d'image de test")
                else:
                    cv2.imwrite("test_image.jpg", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                    print("Image capturée et sauvegardée sous 'test_image.jpg'")
                    logger.info("Image de test capturée avec succès")
                    print("Pour télécharger l'image, utilisez SCP ou SFTP (voir instructions).")
            except Exception as e:
                logger.error(f"Erreur lors du test de la caméra : {e}")
                print(f"Erreur test caméra : {e}")

        else:
            logger.warning(f"Choix invalide : {choix}")
            print("Choix invalide. Veuillez entrer un numéro entre 0 et 6, 'k', ou 't'.")

    logger.info("Programme terminé")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Programme interrompu par l'utilisateur")
        print("\nInterruption détectée. Arrêt du robot...")
        try:
            robot = Robot2IN013()
            if robot.distanceSensor is None:
                print("⚠️ Le capteur de distance n’a pas été détecté au démarrage.")

            robot.stop()
            robot.stop_recording()
        except Exception as e:
            logger.error(f"Erreur arrêt robot : {e}")
    except Exception as e:
        logger.error(f"Erreur inattendue : {e}")
        print(f"Erreur : {e}")
        try:
            robot = Robot2IN013()
            robot.stop()
            robot.stop_recording()
        except Exception as e:
            logger.error(f"Erreur arrêt robot : {e}")
