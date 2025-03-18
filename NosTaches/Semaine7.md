🔹 Travaux Réalisés

✅ Calcul des déplacements et des vitesses :

    Ajout de getAngleParcouru pour calculer l’angle parcouru.
    Implémentation de getDistanceParcourue pour mesurer la distance parcourue.
    Ajout de getVitesseG et getVitesseD pour calculer la vitesse des roues.
    Synchronisation des vitesses angulaires avec setVitAng.

✅ Gestion des stratégies de déplacement :

    Création et ajout des stratégies :
        StrategieAvancer (constructeur, start, step, stop).
        StrategieTourner (start, step, stop).
        StrategieAuto (start, step, stop).
        StrategieSeq (start, step, stop).

✅ Ajout d'une gestion avancée des stratégies via le contrôleur :

    Création du fichier controleur.py et de la classe Controler.
    Implémentation de mainControleur() pour exécuter les stratégies en boucle.
    Ajout de lancerStrategie() pour démarrer une nouvelle stratégie.

✅ Améliorations de l’environnement et du robot :

    Création du fichier robot.py et implémentation du constructeur de Robot.
    Ajout de la fonction refresh pour mettre à jour la position et l’orientation du robot.
    Ajout de la fonction avoidObstacle pour gérer la détection d'obstacles.
    Ajout de getDistance pour mesurer la distance jusqu'au plus proche obstacle.
    Ajout de la fonction normaliserVecteur(v) dans utils.py pour normaliser les vecteurs.

✅ Améliorations de l’affichage et de l’environnement :

    Modification de mettre_a_jour dans affichage.py.
    Ajout de la fonction refreshEnvironnement pour actualiser l'affichage.
    Ajout d’une fonction pour initialiser les bordures de l’environnement.
    Modification de handle_events pour mieux gérer les interactions.

✅ Modification et ajout de tests unitaires pour :

    Robot
    Environnement
    Affichage
    Controleur
    Adaptateur

✅ Ajout de fichiers structurants :

    __init__.py dans robot.
    adapt.py pour gérer l’adaptateur simulé.
    test_adapt.py pour tester Adaptateur_simule.
