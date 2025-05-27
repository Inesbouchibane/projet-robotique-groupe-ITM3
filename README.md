 # projet-robotique-groupe-ITM3
![71fYJdrZmCL-removebg-preview](https://github.com/user-attachments/assets/28251d16-a240-4e61-83e9-a8ac9b1dd85c)


# 🤖 LU2IN013 – Projet Robotique (Groupe **ITM3**)

> Contrôlez un **GoPiGo3** dans le monde réel *et* dans deux simulateurs (2D & 3D) – 100 % Python.

---

## 👥 Équipe ITM3
- **Ines Bouchibane** · [@Inesbouchibane](https://github.com/Inesbouchibane)
- **Takoua Hadj Ali** · [@Takoua123](https://github.com/Takoua123)
- **Meriem Berrah** · [@meriem2130](https://github.com/meriem2130)
- **Mouna Bahamid** · [@mouna2235677890](https://github.com/mouna2235677890)
- **Mohamed Bouzekri** · [@bouzekrimohamed](https://github.com/bouzekrimohamed)

---

## 🛠 Installation rapide

```bash
sudo apt-get install python3-tk libasound-dev
pip install -r requirements.txt  # ou :
# pip install pygame panda3d simpleaudio opencv-python numpy easygopigo3
```

> **Robot physique** : suivez la doc officielle GoPiGo3 pour configurer `easygopigo3`.

---

## 🎯 Objectifs

### Partie 1 – Simulation
- Interface 2D (Pygame) & 3D (Panda3D)
- Stratégies : avancer, tourner, tracer un carré, arrêt-mur, suivie de balise, contrôle clavier
- Stratégies conditionnelles & boucles (Turing complet)

### Partie 2 – Robot réel & vision
- Portage direct des stratégies sur GoPiGo3
- Interface 3D temps-réel
- Détection + suivi de balise (OpenCV)

---

## 📽️ Démos vidéo

### Robot réel

**Carré 100 mm**  
<video src="https://github.com/Inesbouchibane/projet-robotique-groupe-ITM3/raw/main/src/carre.MP4" width="360" controls></video>

**Carré (grande taille)**  
<video src="https://github.com/Inesbouchibane/projet-robotique-groupe-ITM3/raw/main/src/3EB0839DF1B035603E3FC71.mp4" width="360" controls></video>

**Arrêt mur**  
<video src="https://github.com/Inesbouchibane/projet-robotique-groupe-ITM3/raw/main/src/arret%20mur.MP4" width="360" controls></video>

**Arrêt mur (variante)**  
<video src="https://github.com/Inesbouchibane/projet-robotique-groupe-ITM3/raw/main/src/arret%20mur%26.MP4" width="360" controls></video>

**Suivi de balise**  
<video src="https://github.com/Inesbouchibane/projet-robotique-groupe-ITM3/raw/main/src/balise.MP4" width="360" controls></video>

**Contrôle clavier (i / o / p / l)**  
<video src="https://github.com/Inesbouchibane/projet-robotique-groupe-ITM3/raw/main/src/touches.MP4" width="360" controls></video>

---

### Simulation 2D / 3D

**Carré + collision (2D)**  
<video src="https://github.com/Inesbouchibane/projet-robotique-groupe-ITM3/raw/main/src/AUTO1.mp4" width="360" controls></video>

**Carré + collision (3D)**  
<video src="https://github.com/Inesbouchibane/projet-robotique-groupe-ITM3/raw/main/src/AUTO2.mp4" width="360" controls></video>

---

## 🚀 Lancement

```bash
# Simulateur 2D
python3 main2d.py

# Simulateur 3D
python3 main3d.py

# Robot réel
python3 main_reel.py
```

Touches directes : **i** (avant) • **o** (arrière) • **p** (gauche) • **l** (droite)

---

## 📌 Liens utiles
- Trello : https://trello.com/b/0Cys3vIn/organisation-de-projet-robotique
- Présentation Canva : https://www.canva.com/design/DAGoomtzC5g/no0mUWsjIIFKdVEOD0xnwA/edit

---

> *« Du code à la réalité : explorez, apprenez, construisez ! »*
