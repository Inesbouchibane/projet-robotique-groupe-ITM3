 Compte Rendu de la Semaine 6

Objectif de la Semaine:

L'objectif de cette semaine était d'améliorer la simulation du robot en ajoutant :
 Une gestion plus fluide des mouvements et rotations.
 Un meilleur contrôle des obstacles et collisions.
 Une amélioration du suivi des distances parcourues.
 Des optimisations dans la gestion des événements et des logs.


Travail Réalisé:

1. Améliorations dans l'Affichage (affichage.py):

Ajout de l'affichage de la distance parcourue par le robot.
Gestion de l'arrêt du robot avec un changement de couleur en jaune lorsqu'il est bloqué.
Amélioration de la gestion du capteur infrarouge (IR) pour afficher un point précis lorsqu'un obstacle est détecté.
Correction d’un bug où la distance parcourue était mal calculée

 2. Ajout d’un Meilleur Contrôle du Robot (robot.py):

Le robot enregistre désormais ses anciennes positions (self.last_x, self.last_y).
Ajout d’une fonction distance_parcourue() pour calculer précisément les distances.
Correction d'un bug où le robot pouvait sortir des limites de la fenêtre (800x600).

 3. Optimisation du Contrôleur (controleur.py):

Meilleure gestion des rotations du robot pour éviter les obstacles en tournant intelligemment.
Ajout d’un log pour suivre les actions importantes, notamment les vitesses et les obstacles détectés.
Nouveau mode avancer_vers_mur_proche() pour que le robot détecte le mur le plus proche et s’y dirige automatiquement.

4. Ajout d'une Meilleure Gestion des Obstacles (environnement.py):

Ajout d’une fonction detecter_murs() pour identifier le mur le plus proche.
Meilleure gestion des obstacles en mode automatique :
Le robot peut changer aléatoirement d’angle lorsqu’un obstacle est trop proche.
Ajout d’un mode d’évitement (self.avoidance_mode) pour contourner les obstacles.

5. Amélioration de l’Interaction Utilisateur (main.py):

Ajout d'un mode "avancer vers un mur" en plus des modes automatique, manuel et carré.
Vérification des entrées utilisateur pour éviter les erreurs lors du choix des vitesses et de la position initiale.


Conclusion 
:
Cette semaine, nous avons apporté plusieurs améliorations à la simulation du robot :
 Un affichage plus informatif (distance parcourue, état du robot, capteur IR).
 Un meilleur contrôle des déplacements et des rotations pour éviter les obstacles.
 Une gestion avancée des collisions et des obstacles avec des réactions intelligentes.
 Un mode supplémentaire pour avancer vers un mur automatiquement.


