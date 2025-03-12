Objectif de la semaine : L'objectif principal de cette semaine était 
d'améliorer la modularité et la flexibilité du code en séparant la logique 
d'affichage (Pygame) du reste du système. Nous avons également visé à 
ajouter de nouvelles fonctionnalités, comme le tracé d'un carré par le 
robot.


Travail Réalisé :

1. Gestion du Dépôt Git :
Une nouvelle branche a été créée dans le dépôt Git pour sauvegarder l'état 
actuel du code. Cela nous permet de travailler sur de nouvelles 
fonctionnalités sans risquer d'endommager la version stable.
 
2. Refactorisation de la Gestion de Pygame : 

Ensuite, nous avons restructuré la gestion de Pygame en centralisant toute 
la logique d'affichage dans une seule fonction et le fichier graphisme.py 
a été restructuré pour que l'affichage soit indépendant du reste de la 
logique.

3. Modification de controleur.py : 

Nous avons également adapté le contrôleur pour qu'il puisse fonctionner 
avec ou sans affichage. Une nouvelle fonctionnalité: tracer_carré, a été 
implémentée dans le contrôleur, permettant au robot de dessiner un carré en se déplaçant de manière autonome.

4. Modification des tests unitaires : 

En parallèle, nous avons commencé à modifier les tests unitaires pour 
qu'ils s'adaptent aux nouvelles fonctionnalités et à la structure 
refactorisée.

