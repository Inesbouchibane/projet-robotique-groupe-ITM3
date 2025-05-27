##### LU2IN013
<div align="center">
      <h1> <img src="https://d29zukiv45njce.cloudfront.net/images/poli.png" width="90px"><br/>Projet S4 Mono-Info 💻</h1>
</div>

[Rapport final](#) | [Diapos Canva](#) *(Liens à compléter avec vos documents)*

# Projet réalisé par
#### [@Inesbouchibane](https://github.com/Inesbouchibane) | [@Takoua123](https://github.com/Takoua123) | [@meriem2130](https://github.com/meriem2130) | [@mouna2235677890](https://github.com/mouna2235677890) | [@bouzekrimohamed](https://github.com/bouzekrimohamed)

---

# Installation

Pour exécuter le projet, assurez-vous d’avoir Python 3 installé, ainsi que les dépendances suivantes. Suivez ces étapes :

1. **Installer les dépendances système** :
   ```bash
   sudo apt-get update
   sudo apt-get install python3-tk libasound-dev
   ```

2. **Installer les bibliothèques Python** :
   ```bash
   pip install pygame panda3d opencv-python numpy easygopigo3
   ```

3. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/[votre-dépôt]/projet-robotique-groupe-ITM3.git
   cd projet-robotique-groupe-ITM3
   ```

4. **Lancer la simulation 2D** :
   ```bash
   python src/main2d.py
   ```

5. **Lancer la simulation 3D** :
   ```bash
   python src/main3d.py
   ```

6. **Contrôler le robot réel** :
   ```bash
   python src/main_reel.py
   ```

*Note* : Pour le robot réel (GoPiGo3), assurez-vous que le matériel est connecté et que la bibliothèque `easygopigo3` est correctement configurée.

---

# Objectifs

Le projet ITM3, réalisé dans le cadre du cours LU2IN013, vise à concevoir un système de contrôle et de simulation pour un robot, à la fois dans un environnement virtuel (2D et 3D) et sur un robot réel (GoPiGo3). Les objectifs sont divisés en deux parties :

### Partie 1 : Simulation
- Développer une **interface de simulation 2D** (Pygame) et **3D** (Panda3D) pour visualiser le robot, ses mouvements, et les obstacles.
- Implémenter des **stratégies de navigation** :
  - Avancer d’une distance donnée.
  - Tourner d’un angle spécifié.
  - Tracer un carré de taille donnée.
  - S’arrêter à une distance précise d’un mur.
  - Suivre une balise colorée via une caméra simulée.
  - Contrôler le robot manuellement via le clavier.
- Gérer les **collisions** avec les murs et les obstacles (rectangle, triangle, cercle) dans l’environnement simulé.

### Partie 2 : Robot réel et fonctionnalités avancées
- Transférer les **stratégies simulées** sur un robot réel (GoPiGo3) équipé d’une caméra, d’un capteur de distance, et d’un IMU.
- Intégrer une **interface 3D** avancée avec Panda3D, permettant de visualiser la trajectoire et la balise.
- Implémenter la **détection de balise** dans l’interface 3D et sur le robot réel, avec un suivi dynamique.
- Ajouter une **fonctionnalité de contrôle clavier** pour un déplacement libre (touches `i`, `o`, `p`, `l`).

---

# Stratégies

Les stratégies suivantes ont été implémentées pour le robot réel et simulé. Chaque stratégie est contrôlable via des interfaces en ligne de commande (`menu_reel.py`), 2D (`menu2d.py`), et 3D (`menu3d.py`).

## Sur le robot réel
Le robot réel utilise un GoPiGo3 avec des capteurs (distance, caméra, IMU) et est contrôlé via `main_reel.py` et `menu_reel.py`.

### Stratégie carré
Le robot trace un carré de 100 mm par côté en combinant des avancées et des rotations de 90°.  
*Exemple attendu* :  
![Stratégie Carré Réel]https://drive.google.com/file/d/1wTKFwo0LAikCaZrNHxjQ630ggcrfyMkM/view?usp=drive_link
### Stratégie arrêt mur
Le robot avance jusqu’à atteindre une distance de 5 mm d’un obstacle, détectée par le capteur de distance.  
*Exemple attendu* :  
![Stratégie Arrêt Mur Réel] https://drive.google.com/file/d/10fwvlYTqn542o7PtIV9_WYqijeySFcep/view?usp=drive_link

### Stratégie suivre balise
Le robot détecte une balise colorée via la caméra et ajuste sa trajectoire pour la suivre.  
*Exemple attendu* :  
![Stratégie Suivre Balise Réel]( https://drive.google.com/file/d/1S82tJFi1JtcsLbh_J4sQsXgOmIjKxlGg/view?usp=drive_link

###Stratégie auto:
Le robot se deplace automatiquement 
https://drive.google.com/file/d/1XR9Z60gZ7JjCNrQX6riTMeJeoIAQKahX/view?usp=drive_link

### Contrôle clavier
Le robot peut être contrôlé manuellement avec les touches `i` (avancer), `o` (reculer), `p` (tourner à gauche), `l` (tourner à droite).  
*Exemple attendu* :  
![Contrôle Clavier Réel]
https://drive.google.com/file/d/1UXJmXbVevL_1didVaoQy1L0jTuRWgZnd/view?usp=drive_link

## Sur le robot simulé
Le robot simulé opère dans un environnement 2D (1000x500) et 3D, avec des obstacles et une balise. Les interfaces 2D (`main2d.py`) et 3D (`main3d.py`) permettent de visualiser les mouvements et les collisions.
##Simulation2d:
https://drive.google.com/file/d/1aAU_e6iWPhPRc1mNkfwJb73F0APVTNJ6/view?usp=sharing
##Simulation3d:
https://drive.google.com/file/d/1f6gIo_Wb7yM6U8XVTaMMZsDtTAxe36tV/view?usp=sharing


# Divers

- **Organisation** : Le projet est géré via une méthodologie Scrum/Agile sur Trello :
  - [Template Trello](https://trello.com/b/OjUJheXD/2i013-template)
  - [Organisation du projet](https://trello.com/b/0Cys3vIn/organisation-de-projet-robotique)
- **Dépôt du cours** : [https://github.com/baskiotisn/2IN013robot2024](https://github.com/baskiotisn/2IN013robot2024)
- **Contact** :
  - Ines Bouchibane : inesbouchibane.de@gmail.com
  - Takoua Hadj Ali : hadjalitakwa7@gmail.com
  - Meriem Berrah : meriembrh6@gmail.com
  - Mouna Bahamid : mounabahamid10@gmail.com
  - Mohamed Bouzekri : lm_bouzekri@esi.dz

---

# Crédits
Projet réalisé par le groupe **ITM3** dans le cadre du cours **LU2IN013** à Sorbonne Université. Merci à notre encadrant pour son soutien et à l’équipe de développement des bibliothèques utilisées (Pygame, Panda3D, easygopigo3).

